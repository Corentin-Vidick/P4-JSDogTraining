# Generated by Django 3.2.17 on 2025-03-08 21:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0003_auto_20250308_1837'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bulkstock',
            name='bulk_name',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='stock.packedstock'),
        ),
        migrations.AlterField(
            model_name='labelstock',
            name='label_name',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='stock.packedstock'),
        ),
    ]
