from django import forms
from .models import Booking, SessionsIndividual, User


class BookingsForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = "__all__"
        exclude = ("name",)

    def __init__(self, *args, **kwargs):
        """
        Filters booked sessions out
        """
        super().__init__(*args, **kwargs)
        day_time = SessionsIndividual.objects.filter(
            booked=False)
        self.fields["session"].queryset = day_time
