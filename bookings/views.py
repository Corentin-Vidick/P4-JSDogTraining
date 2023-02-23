from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic, View
from django.contrib.auth.decorators import login_required
from .models import SessionsIndividual, Booking, Profile, User
from .forms import BookingsForm, ProfileForm


#                                       Show List Of All Possible Sessions
class CreateIndividualSessions(View):
    def get(self, request, *args, **kwargs):
        sessions = SessionsIndividual.objects.all()
        context = {
            'sessions': sessions
        }

        return render(request, "sessions_list.html", context)


#                                       Make A Booking
# Decorator ensures user is logged in,
# otherwise redirects to login page
@login_required(redirect_field_name='/accounts/login')
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


#                                       User Bookings Display
def user_bookings_session(request):
    # Filter so user can only see their own bookings
    user_bookings = Booking.objects.filter(name=request.user.id).all()
    context = {
        "bookings": user_bookings
    }
    return render(request, "user_bookings.html", context)


#                                       User Cancel Booking Button
def cancel_booking(request, booking_id):
    booking_to_delete = get_object_or_404(Booking, id=booking_id)
    # Find corresponding session and update "booked" status to False
    sessions = SessionsIndividual.objects.all()
    for session in sessions:
        if session == booking_to_delete.session:
            x = session
            x.booked = False
            x.save()
    # Delete booking
    booking_to_delete.delete()
    return redirect("user_bookings")


#                                       User Profile Update
# Decorator ensures user is logged in,
# otherwise redirects to login page
@login_required(redirect_field_name='/accounts/login')
def user_profile_update(request):
    print("Creating/updating profile")
    profile = Profile.objects.filter(name=request.user.id).all()
    print(profile)
    profile_form = ProfileForm(request.POST or None, initial={'address_line_1': 'hello'})
    if request.method == "POST":
        if profile_form.is_valid():
            profile_form.instance.user = request.user
            profile_form.instance.name_id = request.user.id
            profile_form.instance.profile_ready = True
            profile_form.save()
        return render(request, 'user_profile.html', {
                    "profile": profile_form,
                    "name_id": request.user
                    })
    template = "user_profile_update.html"
    context = {
        "form": profile_form,
    }
    return render(request, template, context)


#                                       User Profile Display page
@login_required(redirect_field_name='/accounts/login')
def user_profile(request):
    profile = Profile.objects.filter(name=request.user.id).all()
    profile_values = profile.values()
    user_bookings = Booking.objects.filter(name=request.user.id).all()
    return render(request, 'user_profile.html', {
        "profile": profile,
        "profile_values": profile_values,
        "bookings": user_bookings
        })


#                                       User Delete Profile Button
def delete_profile(request):
    print("Deleting profile")
    # profile_to_delete = get_object_or_404(Profile)
    profile_to_delete = Profile.objects.filter(name=request.user.id).all()
    profile_to_delete.delete()

    return redirect("user_profile")
