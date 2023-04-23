from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class ContactMessage(models.Model):
    name = models.CharField(
        max_length=100, null=False, blank=False, default="Guest")
    email = models.CharField(max_length=100, null=False, blank=False)
    message = models.TextField(max_length=1000, null=False, blank=False)

    def __str__(self):
        return f"{self.name}"
