from django.contrib import admin
from .models import SessionsIndividual
from django_summernote.admin import SummernoteModelAdmin


# Register your models here.
@admin.register(SessionsIndividual)
class SessionsAdmin(SummernoteModelAdmin):

    list_filter = ('days', 'confirmed')
    list_display = ('days', 'times', 'confirmed')
    actions = ['approve_session']

    def approve_session(self, request, queryset):
        queryset.update(confirmed=True)
