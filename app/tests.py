"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.test import TestCase
from django.test.client import Client
from django.conf import settings
import simplejson
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from app.models import *
from app.utilities import unique_name, calculate_points
from datetime import datetime, timedelta


def logged_in_client(username=settings.APP_USERNAME,
        password=settings.APP_PASSWORD):
    c = Client()
    c.login(username=username, password=password)
    return c


def check_url_access(url, is_ajax=False, post_required=False):
    access_parameters = {}
    c = Client()
    if is_ajax:
        response = c.get(url, **{'HTTP_X_REQUESTED_WITH':
            'XMLHttpRequest'})
        parsed_data = simplejson.loads(response.content)
        if parsed_data["code"] == settings.APP_CODE["ACCESS DENIED"]:
            access_parameters["ajax_valid"] = True
            access_parameters["ajax_message"] = ""
        else:
            access_parameters["ajax_valid"] = False
            access_parameters["ajax_message"] =\
                'Ajax access error:%s can be accessed without logging in' % url

    if post_required:
        lc = logged_in_client()
        response = lc.get(url)
        if response.status_code == 302 and reverse('invalid_request') in\
                response['Location']:
            access_parameters["post_valid"] = True
            access_parameters["post_message"] = ""
        else:
            access_parameters["post_valid"] = False
            access_parameters["post_message"] =\
                'Post data error:%s can be accessed without post data' % url

    response = c.get(url)
    if response.status_code == 302 and (reverse('access_denied') in \
            response['Location'] or reverse('login') in response['Location']):
        access_parameters["valid"] = True
        access_parameters["message"] = ""
    else:
        access_parameters["valid"] = False
        access_parameters["message"] =\
            'Security access error:%s can be accessed without logging in' % url

    return access_parameters


def verify_json_response(string_data, code):
    data = simplejson.loads(string_data)
    if data["code"] == code:
        return True
    else:
        return False

class VotesTest(TestCase):
    fixtures = ["test_data.json"]
    
    def test_vote(self):
        album = Album.objects.all()[0]
        album_vote, created = AlbumVote.objects.get_or_create(
            key=unique_name("test"), album=album, vote=-1)

    def test_calculate_point(self):
        created_date_new = datetime.now() - timedelta(weeks=12)
        created_date_old = datetime.now() - timedelta(weeks=24)
        votes_new = 100
        votes_old = 150
        points_new = calculate_points(votes_new, created_date_new)
        points_old = calculate_points(votes_old, created_date_old)
        self.assertTrue(points_new > points_old)

    def test_vote_request(self):
        c = logged_in_client()
        album = Album.objects.all()[0]
        vote_album_data = {"vote_type": "album",
                           "vote": 1,
                           "object_id":album.id}
        response = c.post("/vote", vote_album_data)

        album_image = AlbumImage.objects.all()[0]
        vote_album_image_data = {"vote_type": "image",
                           "vote": 1,
                           "object_id":album_image.id}
        response = c.post("/vote", vote_album_image_data)
        response_check = verify_json_response(response.content,
                                            settings.APP_CODE["SERVER MESSAGE"])
        self.assertTrue(response_check)
        