from django.contrib import admin
from .models import SessionsIndividual, Booking
from user_profile.models import Profile
from django_summernote.admin import SummernoteModelAdmin


@admin.register(SessionsIndividual)
class SessionsAdmin(SummernoteModelAdmin):
    """
    Enables CRUD functionalities for SessionsIndividual
    """
    list_filter = ('day', )
    list_display = ('day', 'time', 'booked')


@admin.register(Booking)
class BookingsAdmin(SummernoteModelAdmin):
    """
    Enables CRUD functionalities for Bookings
    """
    list_filter = ('session', 'name')
    list_display = ('name', 'session', 'phone')

    # When booked session is deleted, IndividuallSession.booked's value
    # returns to False
    def delete_queryset(self, request, queryset):

        sessions = SessionsIndividual.objects.all()
        for session in sessions:
            for x in range(len(queryset)):
                if session == queryset[x].session:
                    session.booked = False
                    session.save()
        queryset.delete()
