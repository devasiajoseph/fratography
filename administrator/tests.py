"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

"""
from app.tests import logged_in_client, verify_json_response
from django.test import TestCase
from django.conf import settings
from calendarapp.models import EventObject


class AvailabilityTest(TestCase):
    fixtures = ["test_data.json"]

    def test_remove_availability(self):
        c = logged_in_client()
        available_event = EventObject.objects.filter(
            event_type="availability")[0]
        event_id = available_event.id
        response = c.post("/admin/remove/availability",{"id":event_id})
        response_check = verify_json_response(
            response.content,
            settings.APP_CODE["DELETED"])
        self.assertTrue(response_check)