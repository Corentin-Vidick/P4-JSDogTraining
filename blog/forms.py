from django import forms
from .models import Thought


class CommentForm(forms.ModelForm):
    class Meta:
        model = Thought
        fields = ('body',)
