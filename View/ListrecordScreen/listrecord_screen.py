from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.factory import Factory
from kivy.clock import mainthread
from kivy.properties import ListProperty, ObjectProperty, StringProperty
from kivymd.uix.card import MDCard
from kivymd.uix.recycleboxlayout import MDRecycleBoxLayout
from View.base_screen import BaseScreenView


class RecordCard(RecycleDataViewBehavior, MDCard):
    '''
    To change a viewclass' state as the data assigned to it changes,
    overload the refresh_view_attrs function (inherited from
    RecycleDataViewBehavior)
    '''
    data = ObjectProperty(allownone=True)
    date = StringProperty()
    time = StringProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.handler = None
        # self.data = dict()

    def refresh_view_attrs(self, rv, index, data):
        super().refresh_view_attrs(rv, index, data)
        self.data = data
        self.date = data['created'].strftime("%d, %b %Y")
        self.time = data['created'].strftime("%H:%M %p")
        self.handler = data['handler']

    def on_press(self, *args):
        self.handler(self.data)


class RecordRecycleBoxLayout(MDRecycleBoxLayout):
    pass


class ListrecordScreenView(BaseScreenView):
    results = ListProperty()
    listview = ObjectProperty()

    def model_is_changed(self) -> None:
        """
        Called whenever any change has occurred in the data model.
        The view in this method tracks these changes and updates the UI
        according to these changes.
        """

    def on_enter(self, *args):
        self.controller.refresh_list()

    def handler(self, data):
        user = self.get_global_state('user')
        preview_screen = self.manager.get_screen('preview screen')
        preview_screen.data = data
        report = gen_report(user, data)
        preview_screen.text = report
        self.manager.loc = "preview"

    @mainthread
    def on_results(self, _, results):
        self.listview.data = [
            dict(created=data.created, data=data.data, handler=self.handler) for data in results]


positive_doctor_summary = """
The findings suggest that the patient is likely experiencing a heart attack.  
Immediate medical attention is advised. Begin emergency treatment and monitor the patient closely.  

**Recommendation:**  
Admit to hospital and follow standard heart attack management protocol.
"""

negative_doctor_summary = """
The results do not show signs of a heart attack at this time.  
The patient appears stable and no emergency intervention is needed.  

**Recommendation:**  
Continue regular health check-ups and maintain a healthy lifestyle.
"""


def gen_report(user, _data):
    name = str.upper(user.name or "")
    date = _data['created'].strftime("%d, %b %Y")
    time = _data['created'].strftime("%H:%M %P")
    data = _data['data']['data']
    elapsed = _data['data']['elapsed'] * 10**6
    result = _data['data']['result']
    label = 'POSITIVE' if result['POSITIVE'] > 0.5 else 'NEGATIVE'

    return f"""
================================
Heart Attack Diagnostic Report
================================

**Patient Name:** {name}

**Date:** {date}

**Time:** {time}

----------------------
Patient Responses
----------------------

**How old are you?** {data['age']} years

**Are you male(0) or female(1)?** {"Male" if data['sex'] == 0 else "Female"}

**What is your maximum heart rate during exercise?** {data['max_heart_rate']} bpm

**What is your systolic blood pressure?** {data['systolic_bp']} mmHg

**What is your diastolic blood pressure?** {data['diastolic_bp']} mmHg

**Is your fasting blood sugar above 120 mg/dL?** {"No" if data['fasting_blood_sugar'] == 0 else "Yes"}

**What is your CK-MB level?** {data['ck_mb']} ng/mL

**What is your troponin level?** {data['troponin']} ng/mL

----------------------
Diagnosis Result
----------------------

- **Heart Attack Prediction:** **{label} ({(result[label]*100): .2f}%)**
- **Processing Time:** {elapsed:.3f} microseconds

----------------------
Doctor’s Summary
----------------------
{positive_doctor_summary if label == "POSITIVE" else negative_doctor_summary}
"""
