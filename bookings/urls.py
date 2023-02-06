from . import views
from django.urls import path

urlpatterns = [
    path('', views.CreateIndividualSessions.as_view(), name='home'),
]
