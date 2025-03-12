# Generated by Django 3.2.17 on 2025-03-12 18:57

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0004_auto_20250308_2139'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('label_code', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.RenameField(
            model_name='bulkstock',
            old_name='bulk_quantity',
            new_name='batch',
        ),
        migrations.RemoveField(
            model_name='bulkstock',
            name='bulk_name',
        ),
        migrations.RemoveField(
            model_name='labelstock',
            name='label_name',
        ),
        migrations.RemoveField(
            model_name='packedstock',
            name='category',
        ),
        migrations.RemoveField(
            model_name='packedstock',
            name='label',
        ),
        migrations.RemoveField(
            model_name='packedstock',
            name='name',
        ),
        migrations.RemoveField(
            model_name='packedstock',
            name='origin_stock',
        ),
        migrations.AddField(
            model_name='bulkstock',
            name='expiry_date',
            field=models.DateField(default=datetime.date(2025, 1, 1)),
        ),
        migrations.AddField(
            model_name='bulkstock',
            name='name',
            field=models.CharField(default='Bulk', max_length=100),
        ),
        migrations.AddField(
            model_name='bulkstock',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='labelstock',
            name='label_quantity_1',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='labelstock',
            name='label_quantity_2',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='packedstock',
            name='expiry_date',
            field=models.DateField(default=datetime.date(2025, 1, 1)),
        ),
        migrations.AlterField(
            model_name='packedstock',
            name='weight',
            field=models.IntegerField(help_text='Weight per pack in grams'),
        ),
        migrations.AddField(
            model_name='bulkstock',
            name='products',
            field=models.ManyToManyField(blank=True, related_name='bulk_stocks', to='stock.Product'),
        ),
        migrations.AddField(
            model_name='labelstock',
            name='product',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='label_stock', to='stock.product'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='packedstock',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='packed_stocks', to='stock.product'),
            preserve_default=False,
        ),
    ]
