import threading
from kivy.clock import mainthread
from kivy.properties import ObjectProperty
from kivymd.uix.dialog import MDDialog

from View.base_screen import BaseScreenView
from View.Common.components.basic_dialog import (
    create_success_dialog,
    create_loading_dialog
)
from Utility.status import StatusKind
from .diagnosis_form import DiagnosisForm
from .data import DATA_FIELD


fields = {field['key']: field for field in DATA_FIELD}


class MainScreenView(BaseScreenView):
    loading_dialog: MDDialog | None
    form = ObjectProperty()
    model_status = ObjectProperty(allownone=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.loading_dialog = None
        self.form.fields = fields
        self.last_model_status = None
        self.lock = threading.Lock()

    def model_is_changed(self) -> None:
        """
        Called whenever any change has occurred in the data model.
        The view in this method tracks these changes and updates the UI
        according to these changes.
        """
        # Use as debounce
        self.model_status = self.model.status

    @mainthread
    def on_model_status(self, _, model_status):
        if model_status == StatusKind.IDLE:
            return
        if self.loading_dialog is not None:
            self.disable_form(False)
            self.loading_dialog.dismiss()
            self.loading_dialog = None

        if model_status == StatusKind.LOADING:
            self.disable_form(True)
            self.loading_dialog = create_loading_dialog(
                title="Processing Data",
                msg="Model is running inference on data kindly wait"
            )
            self.loading_dialog.open()
        elif model_status == StatusKind.SUCCESS:
            record = self.model.last_record
            if record:
                label = "POSITIVE" if record.result["POSITIVE"] > 0.5 else "NEGATIVE"
                conf = record.result[label] * 100
                msg = f"Heart Attack Result is {
                    label} with confidence score of {conf:.1f}%"
                dialog = create_success_dialog(
                    title="Inference Complete",
                    msg=msg,
                    action_label="Ok",
                    action=lambda _: self.preview_action(dialog)
                )
                dialog.open()
        elif model_status == StatusKind.ERROR:
            pass

    def disable_form(self, disabled=True):
        objs = [self.ids.form, self.ids.submit]
        for obj in objs:
            obj.disabled = disabled

    def preview_action(self, dialog):
        dialog.dismiss()

    def predict(self):
        data = self.ids.form.get_data()
        self.controller.predict(data)
