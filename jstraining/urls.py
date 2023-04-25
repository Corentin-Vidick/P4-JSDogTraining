from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('summernote/', include('django_summernote.urls')),
    path('accounts/', include('allauth.urls')),
    path('', include('home.urls'), name='home_urls'),
    path('', include('bookings.urls'), name='bookings_urls'),
    path('', include('contact.urls'), name='contact_urls'),
    path('', include('user_profile.urls'), name='user_profile_urls'),
    path('', include('blog.urls'), name='blog_urls'),
]
