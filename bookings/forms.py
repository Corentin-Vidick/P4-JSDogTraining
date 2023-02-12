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
            booked=False)

    # Tims
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields["session"].choices = [["", "Select session date & time"]]
    #     avail_sessions = SessionsIndividual.objects.filter(booked=False)
    #     for session in avail_sessions:
    #         sessions = [
    #             f"{ session.day }",
    #             [[session.day, session.time]
    #                 for s in SessionsIndividual.objects.filter(
    #                     booked=False, day=session.day)]
    #         ]
    #         self.fields["session"].choices.append(sessions)

    # Mine
    # day = forms.ModelChoiceField(queryset=SessionsIndividual.objects.values("day"))
    # time = forms.CharField(label="Time", max_length=20)
    # name = forms.CharField(label="Name", max_length=20)
