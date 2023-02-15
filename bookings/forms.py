from django import forms
from .models import Booking, SessionsIndividual


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


# class DeleteForm(forms.ModelForm):
#     class Meta:
#         model = SessionsIndividual
#         fields = "__all__"

#     def __init__(self, *args, **kwargs):
#         user().__init__(*args, **kwargs)
#         print(model)
