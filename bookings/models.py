from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class SessionsIndividual(models.Model):
    # might need DateField for date
    days = models.CharField(max_length=20, null=False, blank=False)
    times = models.CharField(max_length=20, null=False, blank=False)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"Day: {self.days}     Time: {self.times}"


class Booking(models.Model):
    day = models.CharField(max_length=20, null=False, blank=False)
    time = models.CharField(max_length=20, null=False, blank=False)
    name = models.CharField(max_length=20, null=False, blank=False)

    def __str__(self):
        return f"{self.day}, {self.time}, {self.name}"
