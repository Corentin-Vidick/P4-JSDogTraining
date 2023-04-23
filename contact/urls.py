from . import views
from django.urls import path

urlpatterns = [
    path('contact_us/', views.contact_us,
         name='contact_us'),
    path('contact_success/', views.contact_success,
         name='contact_success'),
]
