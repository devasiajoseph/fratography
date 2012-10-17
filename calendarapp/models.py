from django.db import models


class EventObject(models.Model):
    title = models.CharField(max_length=1024)
    all_day = models.BooleanField(default=False)
    start = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)
    url = models.CharField(max_length=1024)
    class_name = models.CharField(max_length=255)
    editable = models.BooleanField(default=True)
    source = models.CharField(max_length=1024)
    color = models.CharField(max_length=10)
    background_color = models.CharField(max_length=10)
    text_color = models.CharField(max_length=10)
    independent = models.BooleanField(default=False)
    event_type = models.CharField(max_length=50)
