from django.contrib import admin
from .models import SessionsIndividual, Booking
from django_summernote.admin import SummernoteModelAdmin


# Register your models here.
@admin.register(SessionsIndividual)
class SessionsAdmin(SummernoteModelAdmin):

    list_filter = ('days', )
    list_display = ('days', 'times')


@admin.register(Booking)
class BookingsAdmin(SummernoteModelAdmin):

    list_filter = ('day', 'name')
    list_display = ('day', 'time', 'name')
