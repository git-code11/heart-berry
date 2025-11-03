import multitasking
from View.LoginScreen.login_screen import LoginScreenView
from Utility.events import AppEvents
from Utility.status import StatusKind
from libs.db import User


class LoginScreenController:
    """
    The `LoginScreenController` class represents a controller implementation.
    Coordinates work of the view with the model.
    The controller implements the strategy pattern. The controller connects to
    the view to control its actions.
    """

    def __init__(self, model, **kwargs):
        self.model = model  # Model.login_screen.LoginScreenModel
        self.view = LoginScreenView(
            controller=self, model=self.model, **kwargs)

    def get_view(self) -> LoginScreenView:
        return self.view

    @multitasking.task
    def authorize(self, email: str, password: str):
        # check for user existence
        user: User = self.model.get_user_by_email(email)
        if user is None:
            self.view.emit(AppEvents.SnackBar(
                "Account does not exists", StatusKind.WARN))
        else:
            is_valid = user.check_password(password)
            if is_valid:
                self.view.emit(AppEvents.SnackBar(
                    "Authorized", StatusKind.SUCCESS))
                self.view.set_global_state('user', user)
                # self.view.emit(AppEvents.Navigate("main"))
            else:
                self.view.emit(AppEvents.SnackBar(
                    "Invalid", StatusKind.ERROR))
