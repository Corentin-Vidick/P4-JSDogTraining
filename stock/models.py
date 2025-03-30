from django.db import models
import datetime

class Product(models.Model):
    name = models.CharField(max_length=100)
    label_code = models.CharField(max_length=50, unique=True)  # e.g., "FTT", "FTTV", "FF"
    # Other product-specific fields as needed

    def __str__(self):
        return self.name

class PackedStock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='packed_stocks')
    expiry_date = models.DateField(default=datetime.date(2025, 1, 1))
    batch = models.IntegerField()
    quantity = models.IntegerField(default=0)
    weight = models.IntegerField(help_text="Weight per pack in grams")
    # Additional fields if needed

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

class LabelStock(models.Model):
    # Each product has one LabelStock record.
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='label_stock')
    has_two_labels = models.BooleanField(default=False)
    label_quantity_1 = models.IntegerField(default=0)
    label_quantity_2 = models.IntegerField(null=True, blank=True, default=0)
    # Note: Even if there are two labels, they belong exclusively to this product.

    def __str__(self):
        return f"{self.product.name} Labels: Front: {self.label_quantity_1}, Back: {self.label_quantity_2}"

class BulkStock(models.Model):
    # BulkStock is a shared resource.
    name = models.CharField(max_length=100, default="Bulk")  # e.g., "FTT Bulk"
    quantity = models.IntegerField(default=0)  # e.g., available in grams
    expiry_date = models.DateField(default=datetime.date(2025, 1, 1))
    batch = models.IntegerField()
    # A BulkStock can be used for multiple products, and a product can use multiple BulkStock entries.
    products = models.ManyToManyField(Product, related_name='bulk_stocks', blank=True)

    def __str__(self):
        return f"{self.name} - {self.quantity} (Expiry: {self.expiry_date}, Batch: {self.batch})"
