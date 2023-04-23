from django import forms
from .models import Thoughts


class CommentForm(forms.ModelForm):
    class Meta:
        model = Thoughts
        fields = ('body',)
