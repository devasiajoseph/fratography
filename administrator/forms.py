from django import forms
from django.conf import settings
from app.utilities import reply_object
from app.utilities import create_key
from app.models import PriceModel, Availability


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


class AvailabilityForm(forms.Form):
    available_id = forms.IntegerField(widget=forms.HiddenInput,
                                      required=False)
    available_start_date = forms.CharField()
    available_end_date = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super(AvailabilityForm, self).__init__(*args, **kwargs)

    def save_availability(self):
        response = reply_object()
        end_date = self.cleaned_data["available_end_date"]
        if not self.cleaned_data["available_end_date"]:
            end_date = None
        if self.cleaned_data["available_id"]:
            av = Availability.objects.get(pk=self.cleaned_data["available_id"])
            av.available_start_date = self.cleaned_data["available_start_date"]
            av.available_end_date = end_date
            av.save()
            response["code"] = settings.APP_CODE["UPDATED"]
        else:
            av = Availability.objects.create(
                available_start_date=self.cleaned_data["available_start_date"],
                available_end_date=end_date)
            av.save()
            response["code"] = settings.APP_CODE["SAVED"]

        response["id"] = av.id
        response["start"] = av.available_start_date
        response["end"] = av.available_end_date
        return response
