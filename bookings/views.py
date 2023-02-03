from django.shortcuts import render
from .models import SessionsIndividual


# Create your views here.
def get_bookings_sessions(request):
    sessions = SessionsIndividual.objects.all()
    context = {
        'sessions': sessions
    }

    return render(request, "bookings/bookings_list.html", context)
