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

    # When booked session is deleted, IndividuallSession.booked's value
    # returns to False
    def delete_queryset(self, request, queryset):
        
        sessions = SessionsIndividual.objects.all()
        for session in sessions:
            for x in range(len(queryset)):
                if session == queryset[x].session:
                    print("Session found & deleted")
                    session.booked = False
                    session.save()
        # deleted_session = SessionsIndividual.objects.all()
        # deleted_booking = Booking.objects.all()
        # for session in deleted_session:
        #     for booking in deleted_booking:
        #         if booking.session == session:
        #             session.booked = False
        #             session.save()

        queryset.delete()
