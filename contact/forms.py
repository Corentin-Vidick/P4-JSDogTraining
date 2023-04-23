from django import forms
from .models import ContactMessage, User


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = "__all__"
        exclude = ("name",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
