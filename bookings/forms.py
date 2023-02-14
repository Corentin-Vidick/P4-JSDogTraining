from django import forms
from .models import Booking, SessionsIndividual


class BookingsForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = "__all__"
        exclude = ("name",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["session"].queryset = SessionsIndividual.objects.filter(
            booked=False).values_list("day", "time")
