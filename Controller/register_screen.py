import multitasking
from View.RegisterScreen.register_screen import RegisterScreenView
from Model.register_screen import RegisterScreenModel
from Utility.events import AppEvents
from Utility.status import StatusKind


class RegisterScreenController:
    """
    The `RegisterScreenController` class represents a controller implementation.
    Coordinates work of the view with the model.
    The controller implements the strategy pattern. The controller connects to
    the view to control its actions.
    """

    def __init__(self, model: RegisterScreenModel, **kwargs):
        self.model = model  # Model.register_screen.RegisterScreenModel
        self.view = RegisterScreenView(
            controller=self, model=self.model, **kwargs)

    @multitasking.task
    def create_account(self, name: str, email: str, password: str):
        # check for user existence
        exists = self.model.has_user(email)
        if exists:
            self.view.emit(AppEvents.SnackBar(
                "Email Already exists", StatusKind.WARN))
        else:
            user = self.model.create_user(name, email, password)
            if user:
                self.view.emit(AppEvents.SnackBar(
                    "Account Created", StatusKind.SUCCESS))
                self.view.emit(AppEvents.Navigate("login"))

    def get_view(self) -> RegisterScreenView:
        return self.view
