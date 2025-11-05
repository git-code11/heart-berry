
from View.PreviewScreen.preview_screen import PreviewScreenView


class PreviewScreenController:
    """
    The `PreviewScreenController` class represents a controller implementation.
    Coordinates work of the view with the model.
    The controller implements the strategy pattern. The controller connects to
    the view to control its actions.
    """

    def __init__(self, model,  **kwargs):
        self.model = model  # Model.preview_screen.PreviewScreenModel
        self.view = PreviewScreenView(
            controller=self, model=self.model,  **kwargs)

    def get_view(self) -> PreviewScreenView:
        return self.view
