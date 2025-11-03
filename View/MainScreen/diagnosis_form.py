from typing import List, Any
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
import View.Common.components.select_field


class DiagnosisForm(MDBoxLayout):
    fields = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_fields(self, _, fields):
        formFields = []
        for key, value in fields.items():
            field = self.create_field(key, value)
            formFields.append(field)
        self.widgets = formFields

    @staticmethod
    def create_field(key, value):
        field = None
        type_ = value['type']
        if type_ == 'choice' or type_ == 'boolean':
            options = value['options'] if type_ == 'choice' else ['No', 'Yes']
            options = dict(zip(options, range(len(options))))
            field = Factory.SelectField(
                id=key,
                label=value['question'],
                options=options
            )
        else:
            field = Factory.FormField(id=key)
            field.label = value['question']
            field.numeric = type_ == 'number'
        return field

    def get_data(self) -> dict[str, str]:
        data = {field.id: field.value for field in self.widgets}
        # print("DATA =>", data)
        return data
