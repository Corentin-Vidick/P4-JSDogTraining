from django.contrib import admin
from .models import Profile
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Profile)
class ProfileAdmin(SummernoteModelAdmin):
    """
    Enables CRUD functionalities for Profile
    """
    list_display = ('name', 'postcode', 'phone', 'dog_name')
    list_filter = ('name', )
    search_fields = ('name', 'dog_name')
