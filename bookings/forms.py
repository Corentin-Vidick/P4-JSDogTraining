from django import forms
from .models import Booking, SessionsIndividual, Profile


class BookingsForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = "__all__"
        exclude = ("name",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        day_time = SessionsIndividual.objects.filter(
            booked=False).all()
        self.fields["session"].queryset = day_time


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"
        exclude = ("name", "profile_ready")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
