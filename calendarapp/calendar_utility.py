from calendarapp.models import EventObject
from calendarapp.forms import EventObjectForm

# this can be saved in settings
# only provide those settings that are actually required
CALENDAR_SETTINGS = {
    "event_type":
        {
        "availability": {
            "class_name": "available-event",
            "title": "Slot available"
            },
        "booked": {
            "class_name": "booked-event",
            "title": "Booked"
            }
        },
    "date_format":"%Y-%m-%d %H:%M:%S"
    }


class CalendarEvent(object):
    def set_calendar_settings(self):
            if self.independent:
                return
            type_settings = CALENDAR_SETTINGS["event_type"][self.event_type]
            for key in self.__dict__:
                if key in type_settings:
                    setattr(self, key, type_settings[key])
            return

    def format_date(self, raw_date):
        return raw_date.strftime(CALENDAR_SETTING["date_format"])

    def set_event_dict(self, event_object):
        event_dict = {}
        event_dict["id"] = event_object.id
        event_dict["event_type"] = event_object.event_type
        event_dict["title"] = event_object.title
        event_dict["all_day"] = event_object.all_day
        event_dict["start"] = self.format_date(event_object.start)
        event_dict["end"] = self.format_date(event_object.end)
        event_dict["url"] = event_object.url
        event_dict["class_name"] = event_object.class_name
        event_dict["editable"] = event_object.editable
        event_dict["source"] = event_object.source
        event_dict["color"] = event_object.color
        event_dict["background_color"] = event_object.background_color
        event_dict["text_color"] = event_object.text_color
        event_dict["independent"] = event_object.independent
        if not event_object.independent:
            type_settings = CALENDAR_SETTINGS["event_type"][event_object.event_type]
            for key in event_dict:
                if key in type_settings:
                    event_dict[key] = type_settings["key"]
        return event_dict

        

    def set_object(self, event_object):
        self.id = event_object.id
        self.event_type = event_object.event_type
        self.title = event_object.title
        self.all_day = event_object.all_day
        self.start = self.format_date(event_object.start)
        self.end = self.format_date(event_object.end)
        self.url = event_object.url
        self.class_name = event_object.class_name
        self.editable = event_object.editable
        self.source = event_object.source
        self.color = event_object.color
        self.background_color = event_object.background_color
        self.text_color = event_object.text_color
        self.independent = event_object.independent
        self.set_calendar_settings()

    def get_event(self, event_id):
        event_object = EventObject.objects.get(pk=self.id)
        self.set_object(event_object)
        return

    def get_event_json(self, event_id):
        event_object = EventObject.objects.get(pk=self.id)
        self.set_object(event_object)
        return

    def get_events_json(self, event_type_list):
        events = []
        event_objects = EventObject.objects.get(event_type__in=event_type_list)
        for event_object in event_objects:
            events.append(self.set_event_dict)
            
        return events

    def __init__(self, *args, **kwargs):
        self.id = kwargs.pop('id', None)
        if self.id:
            self.get_event(self.id)
            super(CalendarEvent, self).__init__(*args, **kwargs)
        self.event_type = kwargs.pop('event_type', None)
        self.title = kwargs.pop('title', None)
        self.all_day = kwargs.pop('all_day', False)
        self.start = kwargs.pop('start', None)
        self.end = kwargs.pop('end', None)
        self.url = kwargs.pop('url', None)
        self.class_name = kwargs.pop('class_name', None)
        self.editable = kwargs.pop('editable', True)
        self.source = kwargs.pop('source', None)
        self.color = kwargs.pop('color', None)
        self.background_color = kwargs.pop('background_color', None)
        self.text_color = kwargs.pop('text_color', None)
        self.independent = kwargs.pop('independent', False)
        self.set_calendar_settings()
        super(CalendarEvent, self).__init__(*args, **kwargs)

    def save():
        event_object = EventObject.objects.create(
            title=self.title,
            all_day=self.all_day,
            start=self.start,
            end=self.end,
            url=self.url,
            class_name=self.class_name,
            editable=self.editable,
            source=self.source,
            color=self.color if self.independent else None,
            background_color=self.background_color if self.independent else None,
            text_color=self.text_color if self.independent else None,
            independent=self.independent
            )
        event_object.save()
        return event_object
