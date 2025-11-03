import typing as tp
from collections import namedtuple
from enum import Enum
from Utility.status import StatusKind
import time

Event = namedtuple("Event", ["kind", "props"])


class Tracked:
    def __init__(self, data: tp.Any):
        self.time = time.time()
        self.data = data

    @classmethod
    def wrap(cls, data: tp.Any):
        return cls(data)

    def unwrap(self):
        return self.data


class EventKind(Enum):
    NAVIGATE = "NAVIGATE"
    SNACKBAR = "SNACKBAR"
    IDLE = "IDLE"
    START_LOADING = "START_LOADING"
    STOP_LOADING = "STOP_LOADING"
    EXECUTE = "EXECUTE"


class AppEvents:

    def Idle():
        return Event(EventKind.IDLE, None)

    def Navigate(screen: str, data: tp.Any = None):
        return Event(EventKind.NAVIGATE, dict(loc=screen, data=data))

    def SnackBar(msg: str,
                 status: tp.Literal['success', 'info', 'warn', 'error']
                 | StatusKind):
        return Event(EventKind.SNACKBAR, dict(msg=msg, status=status))

    def Trigger(event: EventKind, **kwargs):
        return Event(event, kwargs)

    def StartLoading(title="Processing", msg="Please Wait"):
        return Event(EventKind.START_LOADING, dict(msg=msg, title=title))

    def StopLoading():
        return Event(EventKind.STOP_LOADING, None)

    def Execute(caller: str, *args, **kwargs):
        return Event(EventKind.EXECUTE, dict(caller=caller, args=args, kwargs=kwargs))


IDLE_EVENT = AppEvents.Idle()
