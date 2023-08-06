from .event import Event


class ModuleOpenedEvent(Event):
    local = True

    def __init__(self):
        Event.__init__(self)


__all__ = ['ModuleOpenedEvent']
