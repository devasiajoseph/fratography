from django import forms
from django.conf import settings
from app.utilities import reply_object
from app.utilities import create_key
from app.models import PriceModel


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
    available_end_date = forms.CharField()
