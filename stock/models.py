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
        return f"{self.name}, {self.quantity}"

class BulkStock(models.Model):
    """
    All bulk stock (treats, rope)
    """
    name = models.ForeignKey(
        PackedStock, on_delete=models.CASCADE, null=False, blank=False)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.name}, {self.quantity}"

class LabelStock(models.Model):
    """
    All labels stock
    """
    name = models.ForeignKey(
        PackedStock, on_delete=models.CASCADE, null=False, blank=False)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.name}, {self.quantity}"
