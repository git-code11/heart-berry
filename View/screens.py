# The screen's dictionary contains the objects of the models and controllers
# of the screens of the application.

from Model.main_screen import MainScreenModel
from Controller.main_screen import MainScreenController
from Model.login_screen import LoginScreenModel
from Controller.login_screen import LoginScreenController
from Model.onboarding_screen import OnboardingScreenModel
from Controller.onboarding_screen import OnboardingScreenController
from Model.register_screen import RegisterScreenModel
from Controller.register_screen import RegisterScreenController
from Model.forgotpassword_screen import ForgotpasswordScreenModel
from Controller.forgotpassword_screen import ForgotpasswordScreenController
from Model.listrecord_screen import ListrecordScreenModel
from Controller.listrecord_screen import ListrecordScreenController

screens = {
    'main screen': {
        'model': MainScreenModel,
        'controller': MainScreenController,
    },
    'login screen': {
        'model': LoginScreenModel,
        'controller': LoginScreenController,
    },
    'onboarding screen': {
        'model': OnboardingScreenModel,
        'controller': OnboardingScreenController,
    },
    'register screen': {
        'model': RegisterScreenModel,
        'controller': RegisterScreenController,
    },
    'forgotpassword screen': {
        'model': ForgotpasswordScreenModel,
        'controller': ForgotpasswordScreenController,
    },
    'listrecord screen': {
        'model': ListrecordScreenModel,
        'controller': ListrecordScreenController,
    },
}