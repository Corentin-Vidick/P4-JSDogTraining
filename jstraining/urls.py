from django.contrib import admin
from django.urls import path, include
# from bookings.views import get_bookings_sessions
# from bookings.view import ...

urlpatterns = [
    path('admin/', admin.site.urls),
    path('summernote/', include('django_summernote.urls')),
    path('', include('bookings.urls'), name='bookings_urls'),
    path('', include('blog.urls'), name='blog_urls'),
    path('accounts/', include('allauth.urls')),
]
