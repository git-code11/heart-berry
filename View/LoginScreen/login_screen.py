import typing as tp
from dataclasses import dataclass
from kivy.properties import ObjectProperty
from View.base_screen import BaseScreenView
from Utility.form_validator import FormValidator


@dataclass
class LoginForm:
    email: tp.Annotated[str, "email", "not_empty"]
    password: tp.Annotated[str, ["max_length", 20], ["min_length", 5]]


class LoginScreenView(BaseScreenView):

    email_field = ObjectProperty()
    password_field = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mapped_field = dict(
            email=self.email_field,
            password=self.password_field
        )

    def model_is_changed(self) -> None:
        """
        Called whenever any change has occurred in the data model.
        The view in this method tracks these changes and updates the UI
        according to these changes.
        """

    def validate_form_field(self) -> tuple[LoginForm, bool]:
        data = LoginForm(
            email=self.email_field.text,
            password=self.password_field.text
        )

        errors = FormValidator.validate(data)
        return data, (errors if len(errors) > 0 else None)

    def login_action(self):
        data, errors = self.validate_form_field()
        if errors is None:
            self.controller.authorize(
                data.email, data.password
            )
        else:
            for field in self.mapped_field.values():
                field.helper = ""
            for key, error_msg in errors.items():
                self.mapped_field[key].helper = error_msg
