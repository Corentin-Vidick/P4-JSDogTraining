from django import forms
from .models import PackedStock

class AddStockForm(forms.ModelForm):
    class Meta:
        model = PackedStock
        fields = ['quantity', 'expiry_date', 'batch']