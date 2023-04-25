from . import views
from django.urls import path

urlpatterns = [
    path('bookings_list/', views.book_session,
         name='bookings_list'),
    path('user_bookings/', views.user_bookings_session,
         name='user_bookings'),
    path('cancel/<booking_id>', views.cancel_booking,
         name='cancel'),
]
