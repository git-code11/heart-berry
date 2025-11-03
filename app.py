"""
The entry point to the application.

The application uses the MVC template. Adhering to the principles of clean
architecture means ensuring that your application is easy to test, maintain,
and modernize.
"""
from View.screens import screens
from kivy.clock import Clock, mainthread
from kivy.properties import DictProperty, StringProperty
from kivy.factory import Factory
# from kivymd.tools.hotreload.app import MDApp
# from kivy.factory import Factory
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.navigationbar import MDNavigationBar
from typing import NoReturn
from threading import Thread
from glob import glob
from libs.tflite import TfliteHelper
from kivymd.app import MDApp
from libs import db
from View.Common.components.nav import NavigationItem


class AppScreenManager(MDScreenManager):
    loc = StringProperty()

    def goTo(self, screen_name: str):
        self.current = screen_name

    def goBack(self):
        prev_screen_name = self.previous()
        prev_screen_name = str.rstrip(prev_screen_name, " screen")
        self.loc = prev_screen_name

    def on_loc(self, _, value):
        self.goTo(f'{value} screen')


class HeartApp(MDApp):
    global_state = DictProperty()

    def __init__(self, **kwargs):
        super().__init__(
            icon=r"assets/images/logo.png",
            **kwargs)
        self.global_state = dict()
        self.theme_cls.primary_palette = 'Maroon'
        self.default_screen = "SECURED"
        self.secured_screen_name = "SECURED"

        self.DEBUG = False
        self.FOREGROUND_LOCK = True
        self.KV_FILES = [*glob("**/*.kv", recursive=True)]
        self.AUTORELOADER_IGNORE_PATTERNS = [
            "*.pyc", "*__pycache__*", ".git*", ".venv*", "data.db"
        ]
        # self.CLASSES = {
        #     "LoginScreen": "View.LoginScreen.login_screen",
        #     "RegisterScreen": "View.RegisterScreen.register_screen"
        # }

        if not self.DEBUG:
            self.load_all_kv_files(self.directory)

        # This is the screen manager that will contain all the screens of your
        # application.
        self.heartModel = TfliteHelper(
            r'assets/models/heart.tflite', ["NEGATIVE", "POSITIVE"])
        self.engine = db.init_engine()

    def on_switch_tabs(self, nav: MDNavigationBar, manager: AppScreenManager, item: NavigationItem):
        if item.screen_name == "logout":
            if 'user' in self.global_state:
                self.global_state.pop('user')
            screen_name = "listrecord"
            # Ensures the home loaction is default
            manager.loc = screen_name
            # Ensures the home tab is selected
            result = list(filter(lambda item: item.screen_name ==
                          screen_name, nav.children))

            if len(result) > 0:
                Clock.schedule_once(
                    lambda _: nav.set_active_item(result[0]), 1)
        else:
            manager.loc = item.screen_name

    def build_main_layout(self) -> MDBoxLayout:
        manager = AppScreenManager()

        nav = MDNavigationBar(
            Factory.NavigationItem(
                icon="home",
                text="Home",
                screen_name="listrecord",
                active=True
            ),
            Factory.NavigationItem(
                icon="note",
                text="Checkup",
                screen_name="main"
            ),
            Factory.NavigationItem(
                icon="logout",
                text="Logout",
                screen_name="logout"
            ),
            on_switch_tabs=lambda nav, item, *arg:
            self.on_switch_tabs(nav, manager, item)
        )

        screen_names = ["listrecord", "main"]
        self.generate_application_screens(manager, screen_names)

        layout = MDScreen(
            MDBoxLayout(
                manager,
                nav,
                orientation="vertical"

            ),
            name=f"{self.secured_screen_name} screen"
        )
        return layout

    def build_app(self) -> MDScreenManager:
        self.app_manager = AppScreenManager()
        screen_names = ["onboarding", "register", "login", "forgotpassword"]
        self.generate_application_screens(self.app_manager, screen_names)
        secured_screen = self.build_main_layout()
        self.app_manager.add_widget(secured_screen)
        # Note: the follwoing line is same as assigning a value to the property
        # Clock.schedule_once(lambda _: self.app_manager.setter(
        #     'loc')(None, self.default_screen), 1)
        return self.app_manager

    @mainthread
    def on_global_state(self, _, state):
        current_user = state.get('user')
        current_loc = self.app_manager.loc
        if current_user:
            self.app_manager.loc = self.secured_screen_name
        else:
            if current_loc == self.secured_screen_name:
                self.app_manager.loc = "login"

    def generate_application_screens(self, manager: MDScreenManager, screen_names: list[str]) -> None:
        """
        Creating and adding screens to the screen manager.
        You should not change this cycle unnecessarily. He is self-sufficient.

        If you need to add any screen, open the `View.screens.py` module and
        see how new screens are added according to the given application
        architecture.
        """
        for i, name_screen in enumerate(screen_names):
            name_screen = name_screen + " screen"
            model = screens[name_screen]["model"](self.engine)
            controller = screens[name_screen]["controller"](
                model, name=name_screen)
            view = controller.get_view()
            manager.add_widget(view)

    @mainthread
    def start_app(self):
        Clock.schedule_once(lambda _: self.on_global_state(
            self, self.global_state), 1)

    def load_service(self) -> NoReturn:
        self.heartModel.load_model()
        self.start_app()

    def on_start(self) -> NoReturn:
        Thread(target=self.load_service).start()
