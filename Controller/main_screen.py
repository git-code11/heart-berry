from typing import Any
import multitasking
import numpy as np
from View.MainScreen.main_screen import MainScreenView
from Utility.events import AppEvents
from Utility.status import StatusKind


class MainScreenController:
    """
    The `MainScreenController` class represents a controller implementation.
    Coordinates work of the view with the model.
    The controller implements the strategy pattern. The controller connects to
    the view to control its actions.
    """

    def __init__(self, model, **kwargs):
        self.model = model  # Model.main_screen.MainScreenModel
        self.view = MainScreenView(controller=self, model=self.model, **kwargs)

    def get_view(self) -> MainScreenView:
        return self.view

    @multitasking.task
    def predict(self, data: dict[str, Any]):
        try:
            self.model.loading()
            inputs = list(map(lambda x: float(x), data.values()))
            inputs = np.array(inputs)
            result = self.view.app.heartModel.inference(inputs)
            user = self.view.get_global_state('user')
            if user is None:
                raise Exception("User Not Found")
            self.model.add_result(user.id, data, result)
        except Exception as e:
            self.view.emit(AppEvents.SnackBar(
                f"An error occured: {str(e)}", StatusKind.ERROR
            ))
            self.model.error(e)
