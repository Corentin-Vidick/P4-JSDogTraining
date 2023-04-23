from django.contrib import admin
from .models import SessionsIndividual, Booking, Profile
from contact.models import ContactMessage
from django_summernote.admin import SummernoteModelAdmin


# Register your models here.
@admin.register(SessionsIndividual)
class SessionsAdmin(SummernoteModelAdmin):

    list_filter = ('day', )
    list_display = ('day', 'time', 'booked')


@admin.register(Booking)
class BookingsAdmin(SummernoteModelAdmin):

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


@admin.register(Profile)
class SessionsAdmin(SummernoteModelAdmin):

    list_filter = ('name', )
    list_display = ('name', 'postcode', 'email', 'phone', 'dog_name')


@admin.register(ContactMessage)
class SessionsAdmin(SummernoteModelAdmin):

    list_filter = ('name', )
    list_display = ('name', 'email', 'message')
