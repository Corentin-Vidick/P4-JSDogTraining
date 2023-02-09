from django import forms
from .models import Booking


class BookingsForm(forms.Form):
    day = forms.CharField(label="Day", max_length=20)
    time = forms.CharField(label="Time", max_length=20)
    name = forms.CharField(label="Name", max_length=20)
