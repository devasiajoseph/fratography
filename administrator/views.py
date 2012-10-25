from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from app.utilities import reply_object, create_key
import simplejson
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
import datetime
from administrator.forms import PriceForm
from app.models import PriceModel
from calendarapp.forms import EventObjectForm
from calendarapp.calendar_utility import apply_settings_query
from calendarapp.models import EventObject


def admin_dashboard(request):
    return render_to_response(
        "admin_dashboard.html",
        context_instance=RequestContext(request))


def calendar(request):
    form = EventObjectForm()
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
    form = EventObjectForm(request.POST)
    if form.is_valid():
        event_object = form.save()
        response["code"] = settings.APP_CODE["SAVED"]
    else:
        response["code"] = settings.APP_CODE["FORM ERROR"]
        response["errors"] = form.errors
    return HttpResponse(simplejson.dumps(response))


def available_time_bkp(request):
    response = []
    av = Availability.objects.all()
    for each_av in av:
        event = {}
        event["id"] = each_av.id
        event["title"] = "available"
        event["start"] = each_av.available_start_date.strftime("%Y-%m-%d %H:%M:%S")
        if each_av.available_end_date:
            event["end"] = each_av.available_end_date.strftime("%Y-%m-%d %H:%M:%S")
        response.append(event)
    return HttpResponse(simplejson.dumps(response),
                        mimetype="application/json")


def available_time(request):
    event_objects = EventObject.objects.filter(event_type="availability")
    calendar_events = apply_settings_query(event_objects)
    return HttpResponse(simplejson.dumps(calendar_events),
                        mimetype="application/json")
