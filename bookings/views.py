from django.shortcuts import render

# Create your views here.
def get_bookings_sessions(request):
    return render(request, "bookings/bookings_list.html")