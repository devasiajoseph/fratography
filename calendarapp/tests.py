from django.test import TestCase
from calendarapp.calendar_utility import CALENDAR_SETTINGS
from app.tests import logged_in_client, verify_json_response
from django.test.client import Client
from django.conf import settings


class CalendarTest(TestCase):

    def test_calendar_save(self):
        c = Client()
        cal_event = {"event_type": "availability",
                     "start": "Mon Oct 08 2012 00:00:00",
                     "end": "Mon Oct 09 2012 00:00:00"}
        response = c.post("/admin/save/availability", cal_event)
        response_check = verify_json_response(response.content,
                                              settings.APP_CODE["SAVED"])
        self.assertTrue(response_check)

        response = c.get("/admin/available/time")
        print response.content

    def test_available_time(self):
        c = Client()
        response = c.get("/admin/available/time")
        print response.content
