from django import forms
from .models import Profile, User


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"
        exclude = ("profile_ready", "name",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
