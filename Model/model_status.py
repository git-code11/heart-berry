from Utility.status import StatusKind


class ModelStatus:

    def __init__(self):
        self._status = StatusKind.idle

    @property
    def status(self):
        return self._status

    def loading(self):
        self._status = StatusKind.LOADING

    def success(self):
        self._status = StatusKind.SUCCESS

    def error(self):
        self._status = StatusKind.ERROR

    def idle(self):
        self._status = StatusKind.IDLE
