from . import views
from django.urls import path

urlpatterns = [
    path('user_profile_update/', views.user_profile_update,
         name='user_profile_update'),
    path('user_profile/', views.user_profile,
         name='user_profile'),
    path('delete_profile/', views.delete_profile,
         name='delete_profile'),
]
