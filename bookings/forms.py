from django import forms
from .models import Booking, SessionsIndividual, Profile, Contact, User


class BookingsForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = "__all__"
        exclude = ("name",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        day_time = SessionsIndividual.objects.filter(
            booked=False)
        self.fields["session"].queryset = day_time


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"
        exclude = ("profile_ready",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # name = User.objects.filter(name=User)
        # self.fields["name"].queryset = name
