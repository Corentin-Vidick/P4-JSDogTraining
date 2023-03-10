# Generated by Django 3.2.17 on 2023-02-10 17:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bookings', '0006_auto_20230210_1702'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='day',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='time',
        ),
        migrations.AddField(
            model_name='booking',
            name='address_line_1',
            field=models.CharField(default='address1', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='booking',
            name='address_line_2',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='country',
            field=models.CharField(choices=[('UK', 'United Kingdom'), ('IE', 'Ireland')], default='UK', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='booking',
            name='phone',
            field=models.CharField(default='123456', max_length=25),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='booking',
            name='postcode',
            field=models.CharField(default='BS5 5JH', max_length=8),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='booking',
            name='session',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='bookings.sessionsindividual'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='booking',
            name='name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
