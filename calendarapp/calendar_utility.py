from calendarapp.models import EventObject
from dateutil import parser
import simplejson

# this can be saved in settings
# only provide those settings that are actually required
CALENDAR_SETTINGS = {
    "event":
        {
        "availability": {
            "class_name": "available-event",
            "title": "Slot available",
            "event_type": "availability"
            },
        "booked": {
            "class_name": "booked-event",
            "title": "Booked",
            "event_type": "booked"
            },
        "event": {
            "class_name": "event-event",
            "title": "Event",
            "event_type": "event"
            }
        },
    "date_format": "%Y-%m-%d %H:%M:%S"
    }


def format_date(raw_date):
        return raw_date.strftime(CALENDAR_SETTINGS["date_format"])


def apply_settings(event):
    event_dict = event.__dict__
    event_dict["start"] = format_date(event.start)
    event_dict["end"] = format_date(event.end)
    if event.independent:
        return event
    type_settings = CALENDAR_SETTINGS["event"][event.event_type]
    for key in event_dict:
        if key in type_settings:
            event_dict[key] = type_settings[key]
    del event_dict["_state"]
    return event_dict


def apply_settings_query(query_set):
    events = []
    for event in query_set:
        events.append(apply_settings(event))
    return events


class CalendarObject(object):
    def set_calendar_settings(self):
        if self.independent:
            return
        type_settings = CALENDA_SETTINGS["event"][self.event_type]
        for key in self.__dict__:
            if key in type_settings:
                setattr(self, key, type_settings[key])
        return

    def format_date(self, raw_date):
        return raw_date.strftime(CALENDAR_SETTINGS["date_format"])

    def set_dict(self, event_object):
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
            type_settings = CALENDAR_SETTINGS["event_type"]
            [event_object.event_type]
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

    def get_object(self, event_id):
        event_object = EventObject.objects.get(pk=self.id)
        self.set_object(event_object)
        return

    def get_json(self, event_id):
        event_object = EventObject.objects.get(pk=self.id)
        event_dict = self.set_dict(event_object)
        return simplejson.dumps(event_dict)

    def get_type_json(self, event_type_list):
        events = []
        event_objects = EventObject.objects.get(event_type__in=event_type_list)
        for event_object in event_objects:
            events.append(self.set_event_dict)

        return simplejson.dumps(events)

    def save(self):
        event_object = EventObject.objects.create(
            title=self.title,
            all_day=self.all_day,
            start=self.start,
            end=self.end,
            url=self.url if self.independent else None,
            class_name=self.class_name,
            editable=self.editable,
            source=self.source,
            color=self.color if self.independent else None,
            background_color=self.background_color if self.independent else None,
            text_color=self.text_color if self.independent else None,
            independent=self.independent,
            event_type=self.event_type
            )
        event_object.save()
        return event_object

    def update(self):
        event_object = EventObjects.objects.get(pk=self.id)
        event_object.title = self.title
        event_object.all_day = self.all_day
        event_object.start = self.start
        event_object.end = self.end
        event_object.url = self.url if self.independent else None
        event_object.class_name = self.class_name
        event_object.editable = self.editable
        event_object.source = self.source
        event_object.color = self.color if self.independent else None
        event_object.background_color = self.background_color if self.independent else None
        event_object.text_color = self.text_color if self.independent else None
        event_object.independent = self.independent
        event_object.event_type = self.event_type
        event_object.save()
        return even_object

    def __init__(self, *args, **kwargs):
        self._start = parser.parse(kwargs.pop('start', None))
        self._end = parser.parse(kwargs.pop('end', None))
        self.id = kwargs.pop('id', None)
        self.event_type = kwargs.pop('event_type', "event")
        self.title = kwargs.pop('title', None)
        self.all_day = kwargs.pop('all_day', False)
        self.url = kwargs.pop('url', None)
        self.class_name = kwargs.pop('class_name', None)
        self.editable = kwargs.pop('editable', True)
        self.source = kwargs.pop('source', None)
        self.color = kwargs.pop('color', None)
        self.background_color = kwargs.pop('background_color', None)
        self.text_color = kwargs.pop('text_color', None)
        self.independent = kwargs.pop('independent', False)
        self.set_calendar_settings()

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value):
        self._start = parser.parse(value)

    @start.deleter
    def start(self):
        del self._start

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, value):
        self._end = parser.parse(value)

    @end.deleter
    def end(self):
        del self._end
