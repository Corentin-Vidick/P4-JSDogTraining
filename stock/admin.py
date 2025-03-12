from django.contrib import admin

from .models import Product, PackedStock, BulkStock, LabelStock

admin.site.register(Product)
admin.site.register(PackedStock)
admin.site.register(BulkStock)
admin.site.register(LabelStock)
