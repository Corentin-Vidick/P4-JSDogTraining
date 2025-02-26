from . import views
from django.urls import path

urlpatterns = [
     path('stock/', views.stock,
          name='stock'),
     path('add_stock/', views.add_stock,
          name='add_stock'),
     path('stock/<str:treat_name>/', views.stock_detail,
          name='stock_detail'),
     path('add_stock_detail/', views.add_stock_detail,
          name='add_stock_detail'),
]