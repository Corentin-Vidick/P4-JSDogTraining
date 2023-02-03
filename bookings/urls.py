from . import views
from django.urls import path

urlpatterns = [
    path('', views.PostIndividualSessions.as_view(), name='home'),
]