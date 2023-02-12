from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class SessionsIndividual(models.Model):
    # might need DateField for date
    day = models.CharField(max_length=20, null=False, blank=False)
    time = models.CharField(max_length=20, null=False, blank=False)
    booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.day}, {self.time}"


class Booking(models.Model):
    COUNTRIES = (("UK", "United Kingdom"), ("IE", "Ireland"))
    session = models.ForeignKey(
        SessionsIndividual, on_delete=models.CASCADE, null=False, blank=False)
    name = models.ForeignKey(
        User, on_delete=models.CASCADE, null=False, blank=False)
    address_line_1 = models.CharField(max_length=100, null=False, blank=False)
    address_line_2 = models.CharField(max_length=100, null=True, blank=True)
    postcode = models.CharField(max_length=8, null=False, blank=False)
    country = models.CharField(
        choices=COUNTRIES, max_length=20, null=False, blank=False)
    phone = models.CharField(max_length=25, null=False, blank=False)

    def __str__(self):
        return self.name.username
