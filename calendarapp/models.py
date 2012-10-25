from django.db import models
from dateutil import parser
import simplejson
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver


CALENDAR_SETTINGS = {
    "event":
        {
        "availability": {
            "class_name": "available-event",
            "title": "Slot available",
            },
        "booked": {
            "class_name": "booked-event",
            "title": "Booked"
            },
        "event": {
            "class_name": "event-event",
            "title": "Event"
            }
        },
    "date_format": "%Y-%m-%d %H:%M:%S"
    }


class EventObject(models.Model):
    title = models.CharField(max_length=1024)
    all_day = models.BooleanField(default=False)
    start = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)
    independent = models.BooleanField(default=False)
    editable = models.BooleanField(default=True)
    source = models.CharField(max_length=1024, null=True, blank=True)
    event_type = models.CharField(max_length=50, db_column='event_type')
    url = models.CharField(max_length=1024, null=True, blank=True,
                            db_column='url')
    class_name = models.CharField(max_length=255, null=True, blank=True,
                                   db_column='class_name')
    color = models.CharField(max_length=10, null=True, blank=True,
                              db_column='color')
    background_color = models.CharField(max_length=10, null=True, blank=True,
                                         db_column='background_color')
    text_color = models.CharField(max_length=10, null=True, blank=True,
                                   db_column='text_color')
