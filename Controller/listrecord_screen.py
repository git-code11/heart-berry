
from View.ListrecordScreen.listrecord_screen import ListrecordScreenView


class ListrecordScreenController:
    """
    The `ListrecordScreenController` class represents a controller implementation.
    Coordinates work of the view with the model.
    The controller implements the strategy pattern. The controller connects to
    the view to control its actions.
    """

    def __init__(self, model, **kwargs):
        self.model = model  # Model.listrecord_screen.ListrecordScreenModel
        self.view = ListrecordScreenView(
            controller=self, model=self.model, **kwargs)

    def refresh_list(self):
        user = self.view.get_global_state('user')
        if user:
            results = self.model.get_records(user.id)
            self.view.results = results or []

    def get_view(self) -> ListrecordScreenView:
        return self.view
