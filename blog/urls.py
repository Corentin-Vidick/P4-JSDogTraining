from . import views
from django.urls import path

urlpatterns = [
    path('posts_overview/',
         views.PostOverview.as_view(),
         name='posts_overview'),
    path('<slug:slug>/',
         views.SinglePost.as_view(),
         name='single_post'),
]
