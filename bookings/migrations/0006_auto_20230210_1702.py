# Generated by Django 3.2.17 on 2023-02-10 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0005_booking_booked'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='booked',
        ),
        migrations.AddField(
            model_name='sessionsindividual',
            name='booked',
            field=models.BooleanField(default=False),
        ),
    ]
