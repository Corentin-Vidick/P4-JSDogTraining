from django.db import models

class PackedStock(models.Model):
    """
    All packed stock
    """
    category = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    weight = models.IntegerField()
    label = models.CharField(max_length=20)
    origin_stock = models.CharField(max_length=20)
    quantity = models.IntegerField(default=0)
    expiry_date = models.DateField()
    batch = models.IntegerField()

    def __str__(self):
        return f"{self.name}"

class BulkStock(models.Model):
    """
    All bulk stock (treats, rope)
    """
    bulk_name = models.OneToOneField(
        PackedStock, on_delete=models.CASCADE, null=False, blank=False)
    bulk_quantity = models.IntegerField()

    def __str__(self):
        return f"{self.bulk_name}"

class LabelStock(models.Model):
    """
    All labels stock
    """
    label_name = models.OneToOneField(
        PackedStock, on_delete=models.CASCADE, null=False, blank=False)
    has_two_labels = models.BooleanField(default=False)
    label_quantity_1 = models.IntegerField()
    label_quantity_2 = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.label_name}"
