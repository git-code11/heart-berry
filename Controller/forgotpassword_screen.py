import multitasking
from View.ForgotpasswordScreen.forgotpassword_screen \
    import ForgotpasswordScreenView
from Utility.events import AppEvents
from Utility.status import StatusKind
from libs.db import User


class ForgotpasswordScreenController:
    """
    The `ForgotpasswordScreenController` class represents a controller implementation.
    Coordinates work of the view with the model.
    The controller implements the strategy pattern. The controller connects to
    the view to control its actions.
    """

    def __init__(self, model, **kwargs):
        self.model = model  # Model.forgotpassword_screen.ForgotpasswordScreenModel
        self.view = ForgotpasswordScreenView(
            controller=self, model=self.model, **kwargs)

    def get_view(self) -> ForgotpasswordScreenView:
        return self.view

    @multitasking.task
    def reset_password(self, email: str, password: str):
        # check for user existence
        user: User = self.model.reset_password(email, password)
        if user is None:
            self.view.emit(AppEvents.SnackBar(
                "Account does not exists", StatusKind.WARN))
        else:
            self.view.emit(AppEvents.SnackBar(
                "Password reset done", StatusKind.SUCCESS))
            self.view.emit(AppEvents.Navigate("login"))
