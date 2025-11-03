from collections import namedtuple
from Model.base_model import BaseScreenModel

Record = namedtuple('Record', ['data', 'result', 'elapsed'])


class MainScreenModel(BaseScreenModel):
    """
    Implements the logic of the
    :class:`~View.main_screen.MainScreen.MainScreenView` class.
    """
    records: list[Record] = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_record = None

    def loading(self):
        self.last_record = None
        super().loading()
        self.notify_observers('main screen')

    def add_result(self, user_id, data, result):
        record = Record(data, result['output'], result['elapsed'])
        self.create_record(user_id, record._asdict())
        self.last_record = record
        self.records.append(record)
        self.success()
        self.notify_observers('main screen')

    def error(self, err=None):
        self.last_record = None
        super().error()
        self.notify_observers('main screen')
