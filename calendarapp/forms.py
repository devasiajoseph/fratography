from django import forms


class EventObjectForm(forms.Form):
    title = forms.CharField()
    all_day = forms.BooleanField(required=False)
    start = forms.DateTimeField()
    end = forms.DateTimeField(required=False)
    url = forms.CharField(required=False)
    class_name = forms.CharField(required=False)
    editable = forms.BooleanField(required=False)
    source = forms.CharField(required=False)
    color = forms.CharField(required=False)
    background_color = forms.CharField(required=False)
    text_color = forms.CharField(required=False)
    independent = forms.BooleanField(required=False)
