from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic, View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import SessionsIndividual, Booking, User
from user_profile.models import Profile
from .forms import BookingsForm
from user_profile.forms import ProfileForm


@login_required(redirect_field_name='/accounts/login')
def book_session(request):
    """
    Make A Booking
    Login required
    """
    options = SessionsIndividual.objects.all()
    profile_exists = 0
    profiles = Profile.objects.all()
    for profile in profiles:
        if profile.name == request.user:
            initial_values = {
                'address_line_1': profile.address_line_1,
                'address_line_2': profile.address_line_2,
                'postcode': profile.postcode,
                'country': profile.country,
                'phone': profile.phone
            }
            profile_exists = 1
    if profile_exists:
        booking_form = BookingsForm(request.POST or None,
                                    initial=initial_values)
    else:
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
            messages.success(request,
                             'Your booking has been processed')
            return render(
                    request, 'bookings/confirm_booking.html', {
                        "name": request.user, "session": x
                    })
    template = "bookings/bookings_list.html"
    context = {
        "form": booking_form,
    }
    return render(request, template, context)


@login_required(redirect_field_name='/accounts/login')
def user_bookings_session(request):
    """
    User Bookings Display
    Login required
    """
    # Filter so user can only see their own bookings
    user_bookings = Booking.objects.filter(name=request.user.id)
    context = {
        "bookings": user_bookings
    }
    return render(request, "bookings/user_bookings.html", context)


def cancel_booking(request, booking_id):
    """
    User Cancel Booking Button
    """
    booking_to_delete = get_object_or_404(Booking, id=booking_id)
    # Find corresponding session and update "booked" status to False
    sessions = SessionsIndividual.objects.all()
    for session in sessions:
        if session == booking_to_delete.session:
            x = session
            x.booked = False
            x.save()
    booking_to_delete.delete()
    messages.success(request, 'Booking deleted')
    return redirect("user_bookings")
