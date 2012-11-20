from django import forms
from calendarapp.models import EventObject
from calendarapp.calendar_utility import CALENDAR_SETTINGS
from dateutil import parser


class EventObjectForm(forms.Form):
    id = forms.IntegerField(required=False, widget=forms.HiddenInput)
    title = forms.CharField(required=False)
    all_day = forms.CharField(required=False)
    start = forms.CharField()
    end = forms.CharField(required=False)
    url = forms.CharField(required=False)
    class_name = forms.CharField(required=False)
    editable = forms.BooleanField(required=False)
    source = forms.CharField(required=False)
    color = forms.CharField(required=False)
    background_color = forms.CharField(required=False)
    text_color = forms.CharField(required=False)
    independent = forms.BooleanField(required=False)

    def set_calendar_settings(self, event):
        if self.cleaned_data["independent"]:
            return
        type_settings = CALENDAR_SETTINGS["event"][self.event_type]
        for key in event.__dict__:
            if key in type_settings:
                setattr(event, key, type_settings[key])
        return event

    def __init__(self, *args, **kwargs):
        self.event_type = kwargs.pop('event_type', "event")
        super(EventObjectForm, self).__init__(*args, **kwargs)

    def save(self):
        if self.cleaned_data["id"]:
            return self.update_event()
        else:
            return self.save_event()

    def save_event(self):
        event_object = EventObject.objects.create(
            all_day=self.cleaned_data["all_day"],
            start=parser.parse(self.cleaned_data["start"]),
            end=parser.parse(self.cleaned_data["end"]),
            )
        event_object = self.set_calendar_settings(event_object)
        event_object.save()
        return event_object

    def update_event(self):
        event_object = EventObject.objects.get(pk=self.cleaned_data["id"])
        event_object.title = self.cleaned_data["title"]
        event_object.all_day = self.cleaned_data["all_day"]
        event_object.start = parser.parse(self.cleaned_data["start"])
        event_object.end = parser.parse(self.cleaned_data["end"])
        event_object = self.set_calendar_settings(event_object)
        event_object.save()
        event_obj.save()
        return event_object


class EventModForm(forms.Form):
    def delete_event(self):
        event_object = EventObject.objects.get(pk=self.cleaned_data["id"])
        event_object.delete()
        return self.cleaned_data["id"]