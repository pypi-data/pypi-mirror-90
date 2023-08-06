import datetime
import threading
from typing import Union, Callable, TypeVar, Optional, Type
import logging
import pytz
from astroplan import Observer
from astropy.coordinates import EarthLocation


log = logging.getLogger(__name__)

ObjectClass = TypeVar('ObjectClass')


def get_object(config_or_object: Union[dict, object], object_class: Type[ObjectClass] = None, *args, **kwargs) \
        -> ObjectClass:
    """Creates object from config or returns object directly, both optionally after check of type.

    Args:
        config_or_object: A configuration dict or an object itself to create/check.
        object_class: Class to check object against.

    Returns:
        (New) object (created from config) that optionally passed class check.

    Raises:
        TypeError: If the object does not match the given class.
    """

    if config_or_object is None:
        # nothing to do?
        raise TypeError('No config or object given.')

    elif isinstance(config_or_object, dict):
        # a dict is given, so create object
        obj = create_object(config_or_object, *args, **kwargs)

    else:
        # just use given object
        obj = config_or_object

    # do we need a type check and does the given object pass?
    if object_class is not None and not isinstance(obj, object_class):
        raise TypeError('Provided object is not of requested type %s.' % object_class.__name__)
    return obj


def get_class_from_string(class_name):
    parts = class_name.split('.')
    module_name = ".".join(parts[:-1])
    cls = __import__(module_name)
    for comp in parts[1:]:
        cls = getattr(cls, comp)
    return cls


def create_object(config: dict, *args, **kwargs):
    # get class name
    class_name = config['class']

    # create class
    klass = get_class_from_string(class_name)

    # create object
    return klass(*args, **config, **kwargs)


class Object:
    """Base class for all pyobs objects."""

    def __init__(self, vfs: Union['VirtualFileSystem', dict] = None, timezone: Union[str, datetime.tzinfo] = 'utc',
                 location: Union[str, dict, EarthLocation] = None, *args, **kwargs):
        """Initializes a new pyobs module.

        Args:
            vfs: VFS to use (either object or config)
            timezone: Timezone at observatory.
            location: Location of observatory, either a name or a dict containing latitude, longitude, and elevation.
        """
        from pyobs.vfs import VirtualFileSystem

        # an event that will be fired when closing the module
        self.closing = threading.Event()

        # closing event
        self.closing = threading.Event()

        # child objects
        self._child_objects = []

        # create vfs
        if vfs:
            self.vfs = get_object(vfs)
        else:
            from pyobs.vfs import VirtualFileSystem
            self.vfs = VirtualFileSystem()

        # timezone
        if isinstance(timezone, datetime.tzinfo):
            self.timezone = timezone
        elif isinstance(timezone, str):
            self.timezone = pytz.timezone(timezone)
        else:
            raise ValueError('Unknown format for timezone.')
        log.info('Using timezone %s.', timezone)

        # location
        if location is None:
            self.location = None
        elif isinstance(location, EarthLocation):
            self.location = location
        elif isinstance(location, str):
            self.location = EarthLocation.of_site(location)
        elif isinstance(location, dict):
            self.location = EarthLocation.from_geodetic(location['longitude'], location['latitude'],
                                                        location['elevation'])
        else:
            raise ValueError('Unknown format for location.')

        # create observer
        self.observer: Optional[Observer] = None
        if self.location is not None:
            log.info('Setting location to longitude=%s, latitude=%s, and elevation=%s.',
                     self.location.lon, self.location.lat, self.location.height)
            self.observer = Observer(location=self.location, timezone=timezone)

        # opened?
        self._opened = False

        # thread function(s)
        self._threads = {}
        self._watchdog = threading.Thread(target=self._watchdog_func, name='watchdog')

    def _add_thread_func(self, func: Callable, restart: bool = True):
        """Add a new thread func.

        MUST be called in constructor of derived class or at least before calling open() on the object.

        Args:
            func: Func to add.
            restart: Whether to restart this function.
        """

        # create thread
        t = threading.Thread(target=Object._thread_func, name=func.__name__, args=(func,))

        # add it
        self._threads[t] = (func, restart)

    def open(self):
        """Open module."""

        # start threads and watchdog
        for thread, (target, _) in self._threads.items():
            log.info('Starting thread for %s...', target.__name__)
            thread.start()
        if self._watchdog:
            self._watchdog.start()

        # open child objects
        for obj in self._child_objects:
            if hasattr(obj, 'open'):
                obj.open()

        # success
        self._opened = True

    @property
    def opened(self):
        return self._opened

    def close(self):
        """Close module."""

        # request closing of object (used for long-running methods)
        self.closing.set()

        # close child objects
        for obj in self._child_objects:
            if hasattr(obj, 'close'):
                obj.close()

        # join watchdog and then all threads
        if self._watchdog and self._watchdog.is_alive():
            self._watchdog.join()
        [t.join() for t in self._threads.keys() if t.is_alive()]

    @staticmethod
    def _thread_func(target):
        """Run given function.

        Args:
            target: Function to run.
        """
        try:
            target()
        except:
            log.exception('Exception in thread method %s.' % target.__name__)

    def _watchdog_func(self):
        """Watchdog thread that tries to restart threads if they quit."""

        while not self.closing.is_set():
            # get dead threads that need to be restarted
            dead = {}
            for thread, (target, restart) in self._threads.items():
                if not thread.is_alive():
                    dead[thread] = (target, restart)

            # restart dead threads or quit
            for thread, (target, restart) in dead.items():
                if restart:
                    log.error('Thread for %s has died, restarting...', target.__name__)
                    del self._threads[thread]
                    thread = threading.Thread(target=target, name=target.__name__)
                    thread.start()
                    self._threads[thread] = target
                else:
                    log.error('Thread for %s has died, quitting...', target.__name__)
                    self.quit()
                    return

            # sleep a little
            self.closing.wait(1)

    def check_running(self):
        """Check, whether an object should be closing. Can be polled by long-running methods.

        Raises:
            InterruptedError: Raised when object should be closing.
        """
        if self.closing.is_set():
            raise InterruptedError
        return True

    def _add_child_object(self, config_or_object: Union[dict, object], object_class: ObjectClass = None, **kwargs) \
            -> ObjectClass:
        """Create a new sub-module, which will automatically be opened and closed.

        Args:
            config: Module definition

        Returns:
            The created module.
        """

        # create it
        obj = get_object(config_or_object, object_class=object_class,
                         timezone=self.timezone, location=self.location, **kwargs)

        # add to list
        self._child_objects.append(obj)

        # return it
        return obj


__all__ = ['get_object', 'get_class_from_string', 'create_object', 'Object']
