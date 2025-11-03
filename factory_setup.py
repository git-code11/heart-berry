"""
Register View here to ensure we can use import it from anywhere without import
"""
from kivy.factory import Factory

from .View.MainScreen.main_screen import MainScreenView
# from .View.MainScreen.main_screen import MainScreenView

Factory.register('MainScreenView', cls=MainScreenView)
