from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.template.response import TemplateResponse
from app.utilities import reply_object, create_key
import simplejson
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
import datetime
from administrator.forms import PriceForm, AvailabilityForm, AlbumForm,\
AlbumImageForm
from app.models import PriceModel
from calendarapp.calendar_utility import apply_settings_query
from calendarapp.models import EventObject
from django.views.decorators.csrf import csrf_exempt


def admin_dashboard(request):
    return render_to_response(
        "admin_dashboard.html",
        context_instance=RequestContext(request))


def calendar(request):
    form = AvailabilityForm(event_type="availability")
    return render_to_response(
        'admin_calendar.html',
        context_instance=RequestContext(request, {"form": form}))


def price_perhour(request):
    price = PriceModel.objects.get(
        price_type=settings.PRICE_TYPE["PRICE_PER_HOUR"])
    form = PriceForm(initial={"price": price.price_per_hour})
    return render_to_response(
        'admin_price_perhour.html',
        context_instance=RequestContext(request, {"form": form}))


def save_price_perhour(request):
    form = PriceForm(request.POST)
    response = reply_object()
    if form.is_valid():
        response = form.save_price_per_hour()
    else:
        response["code"] = settings.APP_CODE["FORM ERROR"]
        response["errors"] = form.errors
    return HttpResponse(simplejson.dumps(response))


def save_availability(request):
    response = reply_object()
    form = AvailabilityForm(request.POST, event_type="availability")
    if form.is_valid():
        event_object = form.save()
        response["code"] = settings.APP_CODE["SAVED"]
    else:
        response["code"] = settings.APP_CODE["FORM ERROR"]
        response["errors"] = form.errors
    return HttpResponse(simplejson.dumps(response))


def available_time(request):
    event_objects = EventObject.objects.filter(event_type="availability")
    calendar_events = apply_settings_query(event_objects)
    return HttpResponse(simplejson.dumps(calendar_events),
                        mimetype="application/json")


def album(request):
    form = AlbumForm()
    return TemplateResponse(request, 'admin_album_upload.html',
                            {"form": form})


def album_save(request):
    if not request.POST:
        return HttpResponse("waiting")
    response = reply_object()
    form = AlbumForm(request.POST, request.FILES, request=request)
    print request.FILES
    if form.is_valid():
        response = form.save()
    else:
        response["code"] = settings.APP_CODE["FORM ERROR"]
        response["errors"] = form.errors
    return render_to_response("admin_album_submit.html",
                              {"response_data": simplejson.dumps(response)})


def album_image(request, id=0):
    response = reply_object()
    print id
    if request.POST:
        form = AlbumImageForm(request.POST, request.FILES, request=request)
        if form.is_valid():
            response = form.save()
        else:
            response["code"] = settings.APP_CODE["FORM ERROR"]
            response["errors"] = form.errors
    return HttpResponse(simplejson.dumps(response))
