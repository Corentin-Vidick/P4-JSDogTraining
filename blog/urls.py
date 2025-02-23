from . import views
from django.urls import path

urlpatterns = [
    path('posts_overview/',
         views.PostOverview.as_view(),
         name='posts_overview'),
]
