from django.template import RequestContext
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render_to_response
from django.template.response import TemplateResponse
from django.core import serializers
from app.utilities import reply_object
import simplejson
from administrator.forms import PriceForm, AvailabilityForm, AlbumForm,\
AlbumImageForm, AlbumImageModForm, AlbumModForm, AvailabilityModForm,\
CategoryForm, ObjectModForm
from app.models import PriceModel, Album, AlbumImage, AlbumCategory
from calendarapp.calendar_utility import apply_settings_query
from calendarapp.models import EventObject


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
    price, created = PriceModel.objects.get_or_create(
        price_type=settings.PRICE_TYPE["PRICE_PER_HOUR"])
    if created:
        price.price_per_hour = 0
        price.save()
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

    
def remove_availability(request):
    response = reply_object()
    form = AvailabilityModForm(request.POST)
    if form.is_valid():
        response = form.delete_availability()
        response["code"] = settings.APP_CODE["DELETED"]
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


def album_edit(request, album_id):
    album = Album.objects.get(pk=album_id)
    form = AlbumForm(initial={"id": album.id, "name": album.name})
    return TemplateResponse(request, 'admin_album_upload.html',
                            {"form": form,
                             "album": album})


def album_delete(request):
    response = reply_object()
    form = AlbumModForm(request.POST)
    if form.is_valid():
        response = form.delete_album()
    else:
        response["code"] = settings.APP_CODE["FORM ERROR"]
        response["errors"] = form.errors
    return HttpResponse(simplejson.dumps(response))


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


def album_list(request, page):
    albums = Album.objects.all()
    return TemplateResponse(request, 'admin_album_list.html',
                            {"albums": albums})


def album_image(request):
    response = reply_object()
    if request.POST:
        form = AlbumImageForm(request.POST, request.FILES, request=request)
        if form.is_valid():
            response = form.save()
        else:
            response["code"] = settings.APP_CODE["FORM ERROR"]
            response["errors"] = form.errors
    return HttpResponse(simplejson.dumps(response))


def album_image_delete(request):
    response = reply_object()
    form = AlbumImageModForm(request.POST)
    if form.is_valid():
        response = form.delete_image()
    else:
        response["code"] = settings.APP_CODE["FORM ERROR"]
        response["errors"] = form.errors
    return HttpResponse(simplejson.dumps(response))


def get_album_images(request, album_id):
    album = Album.objects.get(pk=album_id)
    album_images = serializers.serialize(
        'json',
        AlbumImage.objects.filter(album=album))
    return HttpResponse(album_images, mimetype="application/json")


def album_category(request):
    categories = AlbumCategory.objects.filter(parent=None).order_by('name')
    print categories
    
    return TemplateResponse(request, 'admin_album_category.html', {"categories":categories})


def album_category_save(request):
    response = reply_object()
    form = CategoryForm(request.POST)
    if form.is_valid():
        response = form.save()
    else:
        response["code"] = settings.APP_CODE["FORM ERROR"]
        response["errors"] = form.errors
    return HttpResponse(simplejson.dumps(response))


def album_category_get(request):
    response = reply_object()
    category = AlbumCategory.objects.get(pk=request.GET["object_id"])
    response["code"] = settings.APP_CODE["CALLBACK"]
    response["name"] = category.name
    response["object_id"] = category.id
    if not category.parent:
        response["parent"] = 0
    else:
        response["parent"] = category.parent.id
    return HttpResponse(simplejson.dumps(response),
                        mimetype="application/json")


def album_category_delete(request):
    response = reply_object()
    form = ObjectModForm(request.POST, model="AlbumCategory")
    if form.is_valid():
        response = form.delete_object()
    else:
        response["code"] = settings.APP_CODE["FORM ERROR"]
        response["errors"] = form.errors
    return HttpResponse(simplejson.dumps(response))


def album_category_sub(request):
    response = reply_object()
    subcategories = []
    sub_objects = AlbumCategory.objects.filter(
        parent=AlbumCategory.objects.get(pk=request.GET["object_id"]))
    for each_obj in sub_objects:
        dict_sub = {}
        dict_sub["id"] = each_obj.id
        dict_sub["name"] = each_obj.name
        subcategories.append(dict_sub)

    response["code"] = settings.APP_CODE["CALLBACK"]
    response["subcategories"] = subcategories
    return HttpResponse(simplejson.dumps(response),
                        mimetype="application/json")