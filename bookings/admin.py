from django.contrib import admin
from .models import SessionsIndividual, Booking
from django_summernote.admin import SummernoteModelAdmin


# Register your models here.
@admin.register(SessionsIndividual)
class SessionsAdmin(SummernoteModelAdmin):

    list_filter = ('day', )
    list_display = ('day', 'time', 'booked')


@admin.register(Booking)
class BookingsAdmin(SummernoteModelAdmin):

    list_filter = ('session', 'name')
    list_display = ('session', 'name', 'phone')
