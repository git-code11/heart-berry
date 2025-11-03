from kivy.factory import Factory
from kivy.uix.widget import Widget
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.dialog import MDDialog, MDDialogHeadlineText, \
    MDDialogSupportingText, MDDialogButtonContainer, MDDialogContentContainer
from kivymd.uix.boxlayout import MDBoxLayout


def create_loading_dialog(cancel=lambda *_: None) -> MDDialog:
    return MDDialog(
        MDDialogHeadlineText(
            text="Processing Data"
        ),

        MDDialogSupportingText(
            theme_font_size="Custom",
            font_size="16sp",
            text="Model is running inference on data kindly wait"
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


def create_success_dialog(score: float, preview=lambda *_: None) -> MDDialog:
    label = "POSITIVE" if score > 0.5 else "NEGATIVE"
    conf = score*100

    return MDDialog(
        MDDialogHeadlineText(
            text="Inference Complete"
        ),
        MDDialogSupportingText(
            theme_font_size="Custom",
            font_size="16sp",
            bold=True,
            text=f"Heart Attack Result is {label} \
            with confidence score of {conf:.1f}%",
            adaptive_height=True,
            theme_height="Custom",
            size_hint_y=None,
            height="32dp"
        ),
        MDDialogButtonContainer(
            Widget(),
            MDButton(
                MDButtonText(text="Preview", bold=True),
                style="text",
                on_release=preview
            ),
            size_hint_y=None,
            height="32dp"
        ),
        radius="8dp",
        style="outlined",
    )
