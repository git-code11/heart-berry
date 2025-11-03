import typing as tp
from dataclasses import dataclass
from kivy.properties import ObjectProperty
from View.base_screen import BaseScreenView
from Utility.form_validator import FormValidator
from Utility.events import AppEvents


@dataclass
class RegisterForm:
    email: tp.Annotated[str, "email", "not_empty"]
    name: tp.Annotated[str, "not_empty", ["max_length", 22]]
    password: tp.Annotated[str, ["max_length", 20], ["min_length", 5]]


class RegisterScreenView(BaseScreenView):
    name_field = ObjectProperty()
    email_field = ObjectProperty()
    password_field = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mapped_field = dict(
            name=self.name_field,
            email=self.email_field,
            password=self.password_field
        )

    def model_is_changed(self) -> None:
        """
        Called whenever any change has occurred in the data model.
        The view in this method tracks these changes and updates the UI
        according to these changes.
        """
        # on successful signup login

    def validate_form_field(self) -> tuple[RegisterForm, bool]:
        data = RegisterForm(
            email=self.email_field.text,
            name=self.name_field.text,
            password=self.password_field.text
        )

        errors = FormValidator.validate(data)
        return data, (errors if len(errors) > 0 else None)

    def signup_action(self):
        data, errors = self.validate_form_field()
        if errors is None:
            self.controller.create_account(
                data.name, data.email, data.password
            )
        else:
            for field in self.mapped_field.values():
                field.helper = ""
            for key, error_msg in errors.items():
                self.mapped_field[key].helper = error_msg
