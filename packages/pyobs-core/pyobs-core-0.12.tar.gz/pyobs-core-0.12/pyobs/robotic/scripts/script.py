import logging
import threading
from typing import Any, Type, Union, TypeVar, Optional

from astroplan import Observer

from pyobs.comm import Comm
from pyobs.comm.proxy import Proxy
from pyobs.robotic import TaskArchive

log = logging.getLogger(__name__)


ProxyClass = TypeVar('ProxyClass')


class Script:
    def __init__(self, configuration: Any, task_archive: TaskArchive, comm: Comm, observer: Observer, *args, **kwargs):
        """Init Script.

        Args:
            comm: Comm object to use
            observer: Observer to use
        """
        self.exptime_done = 0
        self.configuration = configuration
        self.task_archive = task_archive
        self.comm = comm
        self.observer = observer

    def can_run(self) -> bool:
        """Whether this config can currently run."""
        raise NotImplementedError

    def run(self, abort_event: threading.Event):
        """Run script.

        Args:
            abort_event: Event to abort run.

        Raises:
            InterruptedError: If interrupted
        """
        raise NotImplementedError

    def _check_abort(self, abort_event: threading.Event):
        """Check, whether we can continue with script.

        Args:
            abort_event: Event to abort run.

        Raises:
            InterruptedError: If interrupted
        """

        if abort_event.is_set() or not self.can_run():
            raise InterruptedError

    def get_fits_headers(self, namespaces: list = None) -> dict:
        """Returns FITS header for the current status of this module.

        Args:
            namespaces: If given, only return FITS headers for the given namespaces.

        Returns:
            Dictionary containing FITS headers.
        """
        return {}

    def _get_proxy(self, name: str, proxy_class: Type[ProxyClass]) -> Optional[ProxyClass]:
        """Returns a single proxy.

        Args:
            name: Name of proxy
            proxy_class: Expected class of proxy

        Returns:
            Proxy or None on errors
        """

        # nothing?
        if name is None:
            return None

        # try to get proxy
        try:
            return self.comm.proxy(name, proxy_class)
        except ValueError:
            return None


__all__ = ['Script']
