from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic, View
from .models import SessionsIndividual
from .forms import BookingsForm, Booking


# Create your views here.
class CreateIndividualSessions(View):
    def get(self, request, *args, **kwargs):
        sessions = SessionsIndividual.objects.all()
        context = {
            'sessions': sessions
        }

        return render(request, "sessions_list.html", context)


class BookIndividualSession(View):

    def get(self, request, *args, **kwargs):
        options = SessionsIndividual.objects.all()
        context = {
            'options': options,
            'form': BookingsForm(),
            'booked': False,
        }
        return render(request, "bookings_list.html",  context)

    def post(self, request, *args, **kwargs):
        booking_form = BookingsForm(request.POST)
        if booking_form.is_valid():
            clean = booking_form.cleaned_data
            bkng = Booking(
                day=clean['day'],
                time=clean['time'],
                name=clean['name']
            )
            bk.save()
        else:
            booking_form = BookingsForm()
        return render(request, 'confirm_booking.html', {
            "day": bkng.day, "time": bkng.time, "name": bkng.name}
            )
