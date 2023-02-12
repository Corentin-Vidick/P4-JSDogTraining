from . import views
from django.urls import path

urlpatterns = [
    path('', views.CreateIndividualSessions.as_view(), name='home'),
    # path('bookings_list/', views.BookIndividualSession.as_view(),
    #      name='bookings_list'),
    path('bookings_list/', views.book_session,
         name='bookings_list'),
]
