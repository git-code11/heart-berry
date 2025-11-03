
from View.OnboardingScreen.onboarding_screen import OnboardingScreenView


class OnboardingScreenController:
    """
    The `OnboardingScreenController` class represents a controller implementation.
    Coordinates work of the view with the model.
    The controller implements the strategy pattern. The controller connects to
    the view to control its actions.
    """

    def __init__(self, model, **kwargs):
        self.model = model  # Model.onboarding_screen.OnboardingScreenModel
        self.view = OnboardingScreenView(
            controller=self, model=self.model, **kwargs)

    def get_view(self) -> OnboardingScreenView:
        return self.view
