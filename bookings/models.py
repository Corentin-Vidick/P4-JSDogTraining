from django.db import models
from django.contrib.auth.models import User
# from django.db.models.signals import post_save
# from django.dispatch import receiver
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
        return f"{self.session}"


class Profile(models.Model):
    COUNTRIES = (("UK", "United Kingdom"), ("IE", "Ireland"))
    name = models.OneToOneField(User, on_delete=models.CASCADE)
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

# from : https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
# from : https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html
