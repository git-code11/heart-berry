from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.factory import Factory
from kivy.clock import mainthread
from kivy.properties import ListProperty, ObjectProperty, StringProperty
from kivymd.uix.card import MDCard
from View.base_screen import BaseScreenView
from copy import copy


class RecordCard(RecycleDataViewBehavior, MDCard):
    data = ObjectProperty(allownone=True)
    date = StringProperty()
    time = StringProperty()
    info = None
    '''
    To change a viewclass' state as the data assigned to it changes,
    overload the refresh_view_attrs function (inherited from
    RecycleDataViewBehavior)
    '''

    def refresh_view_attrs(self, rv, index, data):
        self.info = copy(data)
        self.date = data['created'].strftime("%d, %b %Y")
        self.time = data['created'].strftime("%H:%M%p")
        super().refresh_view_attrs(rv, index, data)

    # def on_press(self, *args):
    #     print(self.data, self.date, self.info)
    #     self.info['handler'](self.data)


class ListrecordScreenView(BaseScreenView):
    results = ListProperty()
    listview = ObjectProperty()

    def on_manager(self, _, manager):
        def handler(_, screen):
            self.controller.refresh_list()
        manager.bind(current_screen=handler)

    def model_is_changed(self) -> None:
        """
        Called whenever any change has occurred in the data model.
        The view in this method tracks these changes and updates the UI
        according to these changes.
        """

    def handler(self, data):
        user = self.get_global_state('user')
        screen = Factory.PreviewScreen()
        report = gen_report(user, data)
        screen.text = report
        self.manager.switch_to(screen)

    @mainthread
    def on_results(self, _, results):
        self.listview.data = [
            dict(created=data.created, data=data.data, handler=self.handler) for data in results]


def gen_report(user, data):
    return f"""
Heart Attack Report
===================

Patient: {user.name}
Date: 2025-11-03

Diagnosis Form
-------
Patient experienced chest pain and shortness of breath.
ECG confirmed a heart attack.

Treatment
----------
Given medication and a stent was placed.

Follow-up
----------
Take prescribed medicines and return in 2 weeks.
"""
