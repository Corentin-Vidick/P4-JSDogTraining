from django.shortcuts import render, redirect
from django.views import generic, View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile
from bookings.models import Booking
from .forms import ProfileForm
from bookings.forms import BookingsForm


@login_required(redirect_field_name='/accounts/login')
def user_profile_update(request):
    """
    User Profile Creation and Update
    Login required
    """
    print("Creating/updating profile")
    profile = Profile.objects.filter(name=request.user.id).first()
    profile_form = ProfileForm(request.POST or None, instance=profile)
    if request.method == "POST":
        if profile_form.is_valid():
            profile_form.instance.user = request.user
            profile_form.instance.name_id = request.user.id
            profile_form.instance.profile_ready = True
            profile_form.save()
            messages.success(request, 'Your profiles has been created/updated')
            return redirect("user_profile")
    template = "user_profile/user_profile_update.html"
    context = {
        "form": profile_form,
    }
    return render(request, template, context)


@login_required(redirect_field_name='/accounts/login')
def user_profile(request):
    """
    User Profile Display page
    Login required
    """
    profile = Profile.objects.filter(name=request.user.id)
    profile_values = profile.values()
    user_bookings = Booking.objects.filter(name=request.user.id)
    return render(request, 'user_profile/user_profile.html', {
        "profile": profile,
        "profile_values": profile_values,
        "bookings": user_bookings
        })


@login_required(redirect_field_name='/accounts/login')
def delete_profile(request):
    """
    User Delete Profile Button
    Login required
    """
    profile_to_delete = Profile.objects.filter(name=request.user.id)
    profile_to_delete.delete()
    messages.success(request, 'Your profile has been deleted')
    return redirect("user_profile")
