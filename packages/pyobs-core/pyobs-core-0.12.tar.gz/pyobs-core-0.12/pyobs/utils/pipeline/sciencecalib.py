import logging
from typing import Union, Dict

from pyobs.object import get_object
from pyobs.utils.fits import FilenameFormatter
from pyobs.utils.images import BiasImage, DarkImage, FlatImage, Image
from pyobs.utils.astrometry import Astrometry
from pyobs.utils.photometry import Photometry
from .pipeline import Pipeline

log = logging.getLogger(__name__)


class ScienceCalibration(Pipeline):
    def __init__(self, photometry: Union[dict, Photometry] = None, astrometry: Union[dict, Astrometry] = None,
                 masks: Dict[str, Union[Image, str]] = None, filenames: str = None, *args, **kwargs):
        """Pipeline for science images.

        Args:
            photometry: Photometry object. If None, no photometry is performed.
            astrometry: Astrometry object. If None, no astrometry is performed.
            masks: Dictionary with masks to use for each binning given as, e.g., 1x1.
            *args:
            **kwargs:
        """
        # get photometry and astrometry
        self._photometry = None if photometry is None else get_object(photometry, Photometry)
        self._astrometry = None if astrometry is None else get_object(astrometry, Astrometry)

        # masks
        self._masks = {}
        if masks is not None:
            for binning, mask in masks.items():
                if isinstance(mask, Image):
                    self._masks[binning] = mask
                elif isinstance(mask, str):
                    self._masks[binning] = Image.from_file(mask)
                else:
                    raise ValueError('Unknown mask format.')

        # default filename patterns
        if filenames is None:
            filenames = '{SITEID}{TELID}-{INSTRUME}-{DAY-OBS|date:}-{FRAMENUM|string:04d}-{IMAGETYP|type}01.fits'
        self._formatter = FilenameFormatter(filenames)

    def calibrate(self, image: Image, bias: BiasImage = None, dark: DarkImage = None, flat: FlatImage = None) -> Image:
        """Calibrate a single science frame.

        Args:
            image: Image to calibrate.
            bias: Bias frame to use.
            dark: Dark frame to use.
            flat: Flat frame to use.

        Returns:
            Calibrated image.
        """

        # calibrate and trim to TRIMSEC
        calibrated = image.calibrate(bias=bias, dark=dark, flat=flat).trim()

        # add mask
        binning = '%dx%s' % (image.header['XBINNING'], image.header['YBINNING'])
        if binning in self._masks:
            calibrated.mask = self._masks[binning].copy()
        else:
            log.warning('No mask found for binning of frame.')

        # set (raw) filename
        calibrated.format_filename(self._formatter)
        if 'ORIGNAME' in image.header:
            calibrated.header['L1RAW'] = image.header['ORIGNAME']

        # do photometry and astrometry
        if self._photometry is not None:
            # find stars
            self._photometry.find_stars(calibrated)

            # do astrometry
            if self._astrometry is not None:
                try:
                    self._astrometry.find_solution(calibrated)
                except ValueError:
                    # error message comes from astrometry
                    pass

        # return calibrated image
        return calibrated


__all__ = ['ScienceCalibration']
