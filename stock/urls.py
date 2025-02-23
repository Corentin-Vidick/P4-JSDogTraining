from . import views
from django.urls import path

urlpatterns = [
    path('stock/', views.stock,
         name='stock'),
    path('add_stock/', views.add_stock,
         name='add_stock'),
]