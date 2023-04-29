from django.contrib import admin
from .models import ContactMessage
from django_summernote.admin import SummernoteModelAdmin


@admin.register(ContactMessage)
class ContactMessagesAdmin(SummernoteModelAdmin):
    """
    Enables CRUD functionalities for contact messages
    """
    list_display = ('name', 'email')
    list_filter = ('name', )
    search_fields = ('name', 'email')
