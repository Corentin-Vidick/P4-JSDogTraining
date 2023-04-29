from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class Profile(models.Model):
    """
    Model used for users' profiles
    """
    COUNTRIES = (("UK", "United Kingdom"), ("IE", "Ireland"))
    name = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    address_line_1 = models.CharField(max_length=100, null=False, blank=False)
    address_line_2 = models.CharField(max_length=100, null=True, blank=True)
    postcode = models.CharField(max_length=8, null=False, blank=False)
    country = models.CharField(
        choices=COUNTRIES, max_length=20, null=False, blank=False)
    phone = models.CharField(max_length=25, null=False, blank=False)
    email = models.CharField(max_length=100, null=False, blank=False)
    dog_name = models.CharField(max_length=100, null=False, blank=False)
    dog_breed = models.CharField(max_length=100, null=False, blank=False)
    dog_age = models.CharField(max_length=100, null=False, blank=False)
    profile_ready = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"
