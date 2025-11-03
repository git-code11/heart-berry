
from kivy.factory import Factory
from kivy.uix.widget import Widget
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.dialog import MDDialog, MDDialogHeadlineText, \
    MDDialogSupportingText, MDDialogButtonContainer, MDDialogContentContainer
from kivymd.uix.boxlayout import MDBoxLayout


def create_loading_dialog(title="Processing", msg="Please Wait") -> MDDialog:
    return MDDialog(
        MDDialogHeadlineText(
            text=title
        ),

        MDDialogSupportingText(
            theme_font_size="Custom",
            font_size="16sp",
            text=msg
        ),
        MDDialogContentContainer(
            MDBoxLayout(
                Widget(),
                Factory.LoadingHeart(),
                Widget(),
                adaptive_height=True
            ),
        ),
        radius="8dp",
        style="outlined",
        auto_dismiss=False
    )


def create_success_dialog(title, msg, action_label="dismiss", action=None) -> MDDialog:
    if action is None:
        def dismiss():
            dialog.dismiss()

    dialog = MDDialog(
        MDDialogHeadlineText(
            text=title
        ),
        MDDialogSupportingText(
            theme_font_size="Custom",
            font_size="16sp",
            bold=True,
            text=msg,
            adaptive_height=True,
            theme_height="Custom",
            size_hint_y=None,
            height="32dp"
        ),
        MDDialogButtonContainer(
            Widget(),
            MDButton(
                MDButtonText(text=action_label, bold=True),
                style="text",
                on_release=action
            ),
            size_hint_y=None,
            height="32dp"
        ),
        radius="8dp",
        style="outlined",
    )

    return dialog
