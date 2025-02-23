from django.contrib import admin

from .models import PackedStock, BulkStock, LabelStock

admin.site.register(PackedStock)
admin.site.register(BulkStock)
admin.site.register(LabelStock)
