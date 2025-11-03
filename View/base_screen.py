import typing as tp
from kivy.properties import ObjectProperty
from kivy.clock import mainthread

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from Utility.observer import Observer
from Utility.status import StatusSnackBar
from Utility.events import Event, EventKind, IDLE_EVENT
from View.Common.components.basic_dialog import create_loading_dialog


class BaseScreenView(MDScreen, Observer):
    """
    A base class that implements a visual representation of the model data.
    The view class must be inherited from this class.
    """

    controller = ObjectProperty()
    """
    Controller object - :class:`~Controller.controller_screen.ClassScreenControler`.

    :attr:`controller` is an :class:`~kivy.properties.ObjectProperty`
    and defaults to `None`.
    """

    model = ObjectProperty()
    """
    Model object - :class:`~Model.model_screen.ClassScreenModel`.

    :attr:`model` is an :class:`~kivy.properties.ObjectProperty`
    and defaults to `None`.
    """

    view_event = ObjectProperty()

    loading = ObjectProperty(allownone=True)

    def __init__(self, **kw):
        super().__init__(**kw)
        # Often you need to get access to the application object from the view
        # class. You can do this using this attribute.
        self.app = MDApp.get_running_app()
        # Adding a view class as observer.
        self.model.add_observer(self)
        self.snackbar = StatusSnackBar()

    def get_global_state(self, name: str):
        return self.app.global_state.get(name, None)

    def set_global_state(self, name: str, value: tp.Any):
        self.app.global_state[name] = value

    @mainthread
    def emit(self, event: Event):
        self.view_event = event

    def on_view_event(self, _, event: Event | None):
        if event is IDLE_EVENT:
            return

        elif event.kind == EventKind.NAVIGATE:
            loc = event.props.get("loc")
            self.manager.loc = loc

        elif event.kind == EventKind.SNACKBAR:
            msg = event.props.get('msg')
            status = event.props.get('status')
            func = self.snackbar.from_status(status)
            func(text=msg).open()

        elif event.kind == EventKind.START_LOADING:
            if not self.loading:
                self.loading = create_loading_dialog(
                    event.props.get('title'), event.props.get('msg'))
                self.loading.open()

        elif event.kind == EventKind.STOP_LOADING:
            if self.loading:
                self.loading.dismiss()
                self.loading = None

        elif event.kind == EventKind.EXECUTE:
            func = getattr(event.get('caller'))
            func(*event.get('args'), **event.get('kwargs'))

        self.view_event = IDLE_EVENT  # Ensures that same event can be called
