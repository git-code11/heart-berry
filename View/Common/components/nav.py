from kivymd.uix.behaviors import DeclarativeBehavior
from kivymd.uix.navigationbar import MDNavigationItem
from kivy.properties import StringProperty


class NavigationItem(MDNavigationItem):
    icon = StringProperty()
    text = StringProperty()
    screen_name = StringProperty()
