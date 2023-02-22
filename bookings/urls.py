from . import views
from django.urls import path

urlpatterns = [
    path('', views.CreateIndividualSessions.as_view(), name='home'),
    path('bookings_list/', views.book_session,
         name='bookings_list'),
    path('user_bookings/', views.user_bookings_session,
         name='user_bookings'),
    path('sessions_list/', views.CreateIndividualSessions.as_view(),
         name='home'),
    path('cancel/<booking_id>', views.cancel_booking, name='cancel'),
    path('user_profile_update/', views.user_profile_update, name='user_profile_update'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('delete_profile/', views.delete_profile, name='delete_profile'),
]
