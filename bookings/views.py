from django.shortcuts import render
from django.views import generic, View
from .models import SessionsIndividual


# Create your views here.
class IndividualSessions(generic.ListView):
    model = SessionsIndividual
    queryset = SessionsIndividual.objects
    template_name = 'bookings_list.html'


class PostIndividualSessions(View):
    def get(self, request, *args, **kwargs):
        sessions = SessionsIndividual.objects.all()
        context = {
            'sessions': sessions
        }

        return render(request, "bookings_list.html", context)
