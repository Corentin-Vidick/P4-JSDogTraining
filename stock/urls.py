from . import views
from django.urls import path

urlpatterns = [
    path('stock/', views.stock,
         name='stock'),
]