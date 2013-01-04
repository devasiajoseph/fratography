from django import forms
from django.conf import settings
from django.db.models.loading import get_model
from app.utilities import reply_object
from app.utilities import create_key, unique_name, delete_uploaded_file
from app.models import PriceModel, Album, AlbumImage, AlbumCategory
from calendarapp.forms import EventObjectForm, EventModForm
import os
from PIL import Image, ImageOps
from datetime import datetime


class PriceForm(forms.Form):
    price = forms.DecimalField(decimal_places=2)

    def __init__(self, *args, **kwargs):
        super(PriceForm, self).__init__(*args, **kwargs)

    def save_price_per_hour(self):
        response = reply_object()
        #try:
        if True:
            price_object, created = PriceModel.objects.get_or_create(
                price_type=settings.PRICE_TYPE["PRICE_PER_HOUR"])
            price_object.price_per_hour = self.cleaned_data["price"]
            print price_object.price_per_hour
            price_object.save()
            response["code"] = settings.APP_CODE["SAVED"]
        #except:
        #    response["code"] = settings.APP_CODE["SYSTEM ERROR"]

        return response


class AvailabilityForm(EventObjectForm):

    def save_availability(self):
        response = reply_object()
        event_object = self.save()
        response["code"] = settings.APP_CODE["SAVED"]
        return response


class AvailabilityModForm(EventModForm):
    id = forms.IntegerField()
    
    def delete_availability(self):
        response = reply_object()
        deleted_id = self.delete_event()
        response["code"] = settings.APP_CODE["SAVED"]
        return response


class ImageForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ImageForm, self).__init__(*args, **kwargs)

    def format_image(self, filename, width, prefix):
        format_image_name = settings.UPLOAD_PATH + prefix + "_" + filename
        image = Image.open(settings.UPLOAD_PATH + filename)
        size = image.size
        prop = width / float(image.size[0])
        size = (int(prop * float(image.size[0])),
                int(prop * float(image.size[1])))
        image.thumbnail(size, Image.ANTIALIAS)
        image.save(format_image_name, 'JPEG')
        return prefix + "_" + filename

    def handle_uploaded_file(self, upload):
        upload_ext = os.path.splitext(upload.name)[1]
        generated_filename = unique_name(upload.name) + upload_ext
        upload_filename = settings.UPLOAD_PATH + generated_filename
        out = open(upload_filename, 'wb+')
        for chunk in upload.chunks():
            out.write(chunk)
        out.close()
        return generated_filename

    def delete_file(self, filename, prefixes):
        #try:
        if True:
            os.remove(settings.UPLOAD_PATH + filename)
            for prefix in prefixes:
                os.remove(settings.UPLOAD_PATH + prefix + "_" + filename)
        #except:
        #    pass
        return


class AlbumForm(ImageForm):
    id = forms.IntegerField(required=False, widget=forms.HiddenInput)
    name = forms.CharField()
    cover_photo = forms.FileField(widget=forms.ClearableFileInput(
            attrs={"class": "input-file"}), required=False)

    def clean(self):
        if self.cleaned_data["id"] == 0 or\
                self.cleaned_data["id"] == u'' or\
                self.cleaned_data["id"] == None:
            if not "cover_photo" in self.request.FILES:
                self.errors["cover_photo"] = ("Cover Photo is required"),

        return self.cleaned_data

    def create_cover_photo(self, image):
        cover = self.format_image(image, 200.0, "cover")
        return cover

    def save(self):
        response = reply_object()
        #try:
        if True:
            if self.cleaned_data["id"] == 0 or\
                self.cleaned_data["id"] == u'' or\
                self.cleaned_data["id"] == None:
                album = self.save_album()
                image = self.handle_uploaded_file(
                    self.request.FILES['cover_photo'])
                cover = self.create_cover_photo(image)
                album.cover_photo = cover
                album.image = image
                album.save()
                response["code"] = settings.APP_CODE["SAVED"]
                response["id"] = album.id
            else:
                album = self.update_album()
                if "cover_photo" in self.request.FILES:
                    old_image = album.image
                    image = self.handle_uploaded_file(
                    self.request.FILES['cover_photo'])
                    cover = self.create_cover_photo(image)
                    album.cover_photo = cover
                    album.image = image
                    album.save()
                    self.delete_file(old_image, ["cover"])
                response["code"] = settings.APP_CODE["UPDATED"]
                response["id"] = album.id
        #except:
        #    response["code"] = settings.APP_CODE["SYSTEM ERROR"]
        return response

    def save_album(self):
        album = Album.objects.create(name=self.cleaned_data["name"],
                                     created_date=datetime.now())
        album.save()
        return album

    def update_album(self):
        album = Album.objects.get(pk=self.cleaned_data["id"])
        album.name = self.cleaned_data["name"]
        album.save()
        return album


class AlbumImageForm(ImageForm):
    album_id = forms.IntegerField()
    image = forms.FileField()
    cid = forms.CharField()

    def save(self):
        image = self.handle_uploaded_file(
                    self.request.FILES['image'])
        thumbnail = self.format_image(image, 200.0, "thumbnail")
        preview = self.format_image(image, 100.0, "preview")
        display = self.format_image(image, 500.0, "display")
        album = Album.objects.get(pk=self.cleaned_data["album_id"])
        album_image = AlbumImage.objects.create(album=album,
                                                image=image,
                                                thumbnail=thumbnail,
                                                preview=preview,
                                                display=display)
        album_image.save()
        return [{"name":image,
                 "id":album_image.id,
                 "preview": image,
                 "cid":self.cleaned_data["cid"]}]


class AlbumImageModForm(forms.Form):
    image_id = forms.IntegerField()
    image_cid = forms.CharField()

    def delete_image(self):
        response = reply_object()
        image = AlbumImage.objects.get(pk=self.cleaned_data["image_id"])
        delete_album_image_files(image)
        image.delete()
        response["id"] = self.cleaned_data["image_id"]
        response["cid"] = self.cleaned_data["image_cid"]
        response["code"] = settings.APP_CODE["DELETED"]
        return response


class AlbumModForm(forms.Form):
    id = forms.IntegerField()

    def delete_album(self):
        response = reply_object()
        album = Album.objects.get(pk=self.cleaned_data["id"])
        album_images = AlbumImage.objects.filter(album=album)
        for album_image in album_images:
            delete_album_image_files(album_image)
        album.delete()
        response["code"] = settings.APP_CODE["DELETED"]
        return response


def delete_album_image_files(album_image):
    delete_uploaded_file(album_image.image)
    delete_uploaded_file(album_image.thumbnail)
    delete_uploaded_file(album_image.display)
    delete_uploaded_file(album_image.preview)


class ObjectModForm(forms.Form):
    object_id = forms.IntegerField(required=False)

    def delete_object(self, model_name):
        response = reply_object()
        get_model(model_name, 'app').objects.get(pk=self.cleaned_data["object_id"]).delete()
        response["code"] = settings.APP_CODE["DELETED"]
        return response

    
class CategoryForm(ObjectModForm):
    name = forms.CharField()
    parent = forms.IntegerField()

    def get_parent(self):
        parent = None
        if self.cleaned_data["parent"] != 0:
            parent = AlbumCategory.objects.get(pk=self.cleaned_data["parent"])
        return parent

    def save(self):
        response = reply_object()
        object_id = self.cleaned_data[" object_id"]
        if object_id == 0 or\
           object_id == u'' or\
           object_id == None:
            response = self.save_category()
        else:
            response = self.update_category()

        return response

    def save_category(self):
        response = reply_object()
        parent = self.get_parent()
        if parent:
            level = parent.level + 1
        else:
            level = 0
        album_category = AlbumCategory.object.create(
            name=self.cleaned_data, parent=parent, level=level)
        album_category.save()
        response["code"] = settings.APP_CODE["SAVED"]
        return response

    def update_category(self):
        response = reply_object()
        parent = self.get_parent()
        if parent:
            level = parent.level + 1
        else:
            level = 0
        album_category = AlbumCategory.object.get(pk=self.cleaned_data["object_id"])
        album_category.parent = parent
        album_category.name = self.cleaned_data["name"]
        album_category.level = level
        album_category.save()
        response["code"] = settings.APP_CODE["UPDATED"]
        return response

    def delete_category(self):
        return self.delete_object('AlbumCategory')
