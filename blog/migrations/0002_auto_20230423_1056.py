# Generated by Django 3.2.17 on 2023-04-23 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='preview',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='posts',
            name='slug',
            field=models.SlugField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='posts',
            name='title',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
