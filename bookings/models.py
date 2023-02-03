from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class SessionsIndividual(models.Model):
    # might need DateField for date
    days = models.CharField(max_length=20, null=False, blank=False)
    # or DateTimeField to group date and time
    times = models.CharField(max_length=20, null=False, blank=False)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        # to be modified to return proper string with info necessary
        return f"Day: {self.days}     Time: {self.times}"
