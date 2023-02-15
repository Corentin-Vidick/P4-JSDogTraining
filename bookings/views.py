from django.shortcuts import render, get_object_or_404
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


# class BookIndividualSession(View):

#     def get(self, request, *args, **kwargs):
#         options = SessionsIndividual.objects.all()
#         context = {
#             'options': options,
#             'form': BookingsForm(),
#             'booked': False,
#         }
#         return render(request, "bookings_list.html",  context)

#     def post(self, request, *args, **kwargs):
#         booking_form = BookingsForm(request.POST)
#         if booking_form.is_valid():
#             clean = booking_form.cleaned_data
#             bkng = Booking(
#                 day=clean['day'],
#                 time=clean['time'],
#                 name=clean['name']
#             )
#             bkng.save()
#             return render(
#                 request, 'confirm_booking.html', {
#                     "day": bkng.day, "time": bkng.time, "name": bkng.name
#                 }
#             )

#         else:
#             booking_form = BookingsForm()
#             return render(request, "bookings_list.html",  context)


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
    user_bookings = Booking.objects.all()
    # for booking in user_bookings:
    #     n = booking.name
    #     s = booking.session
    context = {
        # "name": n,
        # "session": s,
        "bookings": user_bookings
    }
    return render(request, "user_bookings.html", context)


# def delete_booking(request):
#     print("deleting booked session through user")
#     if request.method == "GET":
#         dest = Booking.objects.all()
#         print(dest)
    # booking = SessionsIndividual.objects.all()
    # user_bookings = Booking.objects.all()
    # delete_booking_form = DeleteForm(request.POST or None)
    # if (request.POST.get('user_booking_delete')):
    #     print(booking)
    # context = {"bookings": user_bookings}
    # return render(request, "user_bookings.html", context)
