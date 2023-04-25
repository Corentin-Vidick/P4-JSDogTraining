from django.db import models
from cloudinary.models import CloudinaryField


class SessionsIndividual(models.Model):
    day = models.CharField(max_length=20, null=False, blank=False)
    time = models.CharField(max_length=20, null=False, blank=False)
    booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.day}, {self.time}"
