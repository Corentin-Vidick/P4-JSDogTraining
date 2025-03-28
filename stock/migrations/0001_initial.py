# Generated by Django 3.2.17 on 2025-02-23 12:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PackedStock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=20)),
                ('weight', models.IntegerField()),
                ('label', models.CharField(max_length=20)),
                ('origin_stock', models.CharField(max_length=20)),
                ('quantity', models.IntegerField(default=0)),
                ('expiry_date', models.DateField()),
                ('batch', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='LabelStock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock.packedstock')),
            ],
        ),
        migrations.CreateModel(
            name='BulkStock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock.packedstock')),
            ],
        ),
    ]
