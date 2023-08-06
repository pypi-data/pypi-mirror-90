from .IRoof import IRoof
from .IAltAz import IAltAz


class IDome(IRoof, IAltAz):
    """Base interface for all shelters with a rotating dome."""

    pass


__all__ = ['IDome']
