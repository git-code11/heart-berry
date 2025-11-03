from kivy.properties import ObjectProperty, DictProperty, StringProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu


class SelectField(MDBoxLayout):
    drop_text = ObjectProperty()
    options = DictProperty()
    value = ObjectProperty()
    label = StringProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        initial_value = list(self.options.items())[0]
        self.drop_text.text = initial_value[0]
        self.value = initial_value[1]

    def open_menu(self, item):
        menu_items = [
            {
                "text": f"{key}",
                "on_release": lambda key=key, value=value: self.menu_callback(key, value),
            } for (key, value) in self.options.items()
        ]
        MDDropdownMenu(caller=item, items=menu_items).open()

    def menu_callback(self, text_item, value):
        self.drop_text.text = text_item
        self.value = value
