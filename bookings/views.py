from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic, View
from .models import SessionsIndividual, Booking
from .forms import BookingsForm


# Create your views here.
class CreateIndividualSessions(View):
    def get(self, request, *args, **kwargs):
        sessions = SessionsIndividual.objects.all()
        context = {
            'sessions': sessions
        }

        return render(request, "sessions_list.html", context)


def book_session(request):
    options = SessionsIndividual.objects.all()
    booking_form = BookingsForm(request.POST or None)
    if request.method == "POST":
        if booking_form.is_valid():
            # Finds corresponding sessions in SessionsIndividual
            # and sets its value to True
            for session in options:
                if booking_form.instance.session == session:
                    x = session
                    x.booked = True
                    x.save()
            booking_form.instance.name = request.user
            booking_form.save()
        return render(
                request, 'confirm_booking.html', {
                    "name": request.user, "session": x
                })
    template = "bookings_list.html"
    context = {
        "form": booking_form,
    }
    return render(request, template, context)


def user_bookings_session(request):
    # Filter so user can only see their own bookings
    user_bookings = Booking.objects.filter(name=request.user.id).all()
    print(user_bookings)
    context = {
        "bookings": user_bookings
    }
    return render(request, "user_bookings.html", context)


def cancel_booking(request, booking_id):
    print("canceling booking")
    booking_to_delete = get_object_or_404(Booking, id=booking_id)
    print(type(booking_to_delete))
    # Find corresponding session and update "booked" status to False
    sessions = SessionsIndividual.objects.all()
    for session in sessions:
        if session == booking_to_delete.session:
            print("booking to delete and session matched")
            x = session
            x.booked = False
            x.save()
    # Delete booking
    booking_to_delete.delete()
    return redirect("user_bookings")
