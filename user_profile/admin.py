from django.contrib import admin
from .models import Profile
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Profile)
class SessionsAdmin(SummernoteModelAdmin):
    list_display = ('name', 'postcode', 'phone', 'dog_name')
    list_filter = ('name', )
    search_fields = ('name', 'dog_name')
