import io
from enum import Enum

import numpy as np
from astropy.io import fits
from astropy.io.fits import table_to_hdu, ImageHDU
from astropy.table import Table


class Image:
    class CombineMethod(Enum):
        MEAN = 'mean'
        MEDIAN = 'median'
        SIGMA = 'sigma'

    def __init__(self, data: np.ndarray = None, header: fits.Header = None, *args, **kwargs):
        self.data = data
        self.header = fits.Header() if header is None else header
        self.mask = None
        self.catalog = None

        # add basic header stuff
        if data is not None:
            self.header['NAXIS1'] = data.shape[1]
            self.header['NAXIS2'] = data.shape[0]

    @classmethod
    def from_bytes(cls, data) -> 'Image':
        # create hdu
        with io.BytesIO(data) as bio:
            # read whole file
            data = fits.open(bio, memmap=False, lazy_load_hdus=False)

            # load image
            image = cls._from_hdu_list(data)

            # close file
            data.close()
            return image

    @classmethod
    def from_file(cls, filename: str) -> 'Image':
        # open file
        data = fits.open(filename, memmap=False, lazy_load_hdus=False)

        # load image
        image = cls._from_hdu_list(data)

        # close file
        data.close()
        return image

    @classmethod
    def _from_hdu_list(cls, data):
        """Load Image from HDU list.

        Args:
            data: HDU list.

        Returns:
            Image.
        """

        # create image
        image = cls()

        # find HDU with image data
        for hdu in data:
            if isinstance(hdu, fits.PrimaryHDU) and hdu.header['NAXIS'] > 0 or \
                    isinstance(hdu, fits.ImageHDU) and hdu.name == 'SCI' or \
                    isinstance(hdu, fits.CompImageHDU):
                # found image HDU
                image_hdu = hdu
                break
        else:
            raise ValueError('Could not find HDU with main image.')

        # get data
        image.data = image_hdu.data.astype(np.float)
        image.header = image_hdu.header

        # mask
        if 'BPM' in data:
            image.mask = data['BPM'].data

        # catalog
        if 'CAT' in data:
            image.catalog = Table(data['CAT'].data)

        # finished
        return image

    def copy(self):
        img = Image()
        img.data = self.data.copy()
        img.header = self.header
        return img

    def __truediv__(self, other):
        img = self.copy()
        img.data /= other
        return img

    def writeto(self, f, *args, **kwargs):
        # create HDU list
        hdu_list = fits.HDUList([])

        # create image HDU
        hdu = fits.PrimaryHDU(self.data, header=self.header)
        hdu_list.append(hdu)

        # catalog?
        if self.catalog is not None:
            hdu = table_to_hdu(self.catalog)
            hdu.name = 'CAT'
            hdu_list.append(hdu)

        # mask?
        if self.mask is not None:
            hdu = ImageHDU(self.mask.data.astype(np.uint8))
            hdu.name = 'BPM'
            hdu_list.append(hdu)

        # write it
        hdu_list.writeto(f, *args, **kwargs)

    def write_catalog(self, f, *args, **kwargs):
        if self.catalog is None:
            return

        # create HDU and write it
        table_to_hdu(self.catalog).writeto(f, *args, **kwargs)

    def _section(self, keyword: str = 'TRIMSEC') -> np.ndarray:
        """Trim an image to TRIMSEC or BIASSEC.

        Args:
            hdu: HDU to take data from.
            keyword: Header keyword for section.

        Returns:
            Numpy array with image data.
        """

        # keyword not given?
        if keyword not in self.header:
            # return whole data
            return self.data

        # get value of section
        sec = self.header[keyword]

        # split values
        s = sec[1:-1].split(',')
        x = s[0].split(':')
        y = s[1].split(':')
        x0 = int(x[0]) - 1
        x1 = int(x[1])
        y0 = int(y[0]) - 1
        y1 = int(y[1])

        # return data
        return self.data[y0:y1, x0:x1]

    def _subtract_overscan(self):
        # got a BIASSEC?
        if 'BIASSEC' not in self.header:
            return

        # get mean of BIASSEC
        biassec = np.mean(self._section('BIASSEC'))

        # subtract mean
        self.header['L1OVRSCN'] = (biassec, 'Subtracted mean BIASSEC counts')
        self.data -= biassec

    def trim(self):
        # TRIMSEC exists?
        if 'TRIMSEC' in self.header:
            # create new image
            img = self.copy()

            # trim data
            img.data = img._section('TRIMSEC')

            # adjust size in fits headers
            img.header['NAXIS2'], img.header['NAXIS1'] = img.data.shape

            # delete keywords
            for key in ['TRIMSEC', 'BIASSEC', 'DATASEC']:
                if key in img.header:
                    del img.header[key]

            # finished
            return img

        else:
            # don't do anything
            return self

    def calibrate(self, bias: 'BiasFrame' = None, dark: 'DarkFrame' = None, flat: 'FlatFrame' = None):
        # copy image
        img = self.copy()

        # to float32
        img.data = img.data.astype(np.float32)

        # subtract overscan
        img._subtract_overscan()

        # subtract bias
        if bias is not None:
            img.data -= bias.data
            img.header['L1BIAS'] = (bias.header['FNAME'].replace('.fits.fz', '').replace('.fits', ''),
                                    'Name of BIAS frame')

        # subtract dark
        if dark is not None:
            img.data -= dark.data * img.header['EXPTIME']
            img.header['L1DARK'] = (dark.header['FNAME'].replace('.fits.fz', '').replace('.fits', ''),
                                    'Name of DARK frame')

        # divide by flat
        if flat is not None:
            img.data /= flat.data
            img.header['L1FLAT'] = (flat.header['FNAME'].replace('.fits.fz', '').replace('.fits', ''),
                                   'Name of FLAT frame')

        # it's reduced now
        img.header['RLEVEL'] = 1

        # finished
        return img

    def format_filename(self, formatter):
        self.header['FNAME'] = formatter(self.header)

    @property
    def pixel_scale(self):
        """Returns pixel scale in arcsec/pixel."""
        if 'CD1_1' in self.header:
            return abs(self.header['CD1_1']) * 3600.
        elif 'CDELT1' in self.header:
            return abs(self.header['CDELT1']) * 3600.
        else:
            return None


__all__ = ['Image']
