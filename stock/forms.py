from django import forms
from .models import PackedStock

class AddStockForm(forms.ModelForm):
    class Meta:
        model = PackedStock
        fields = ['quantity', 'expiry_date', 'batch']
        widgets = {
            'expiry_date': forms.DateInput(format='%Y-%m-%d', attrs={'placeholder': 'YYYY-MM-DD'}),
        }
        help_texts = {
            'expiry_date': 'Ex: YYYY-MM-DD',
        }

class AddStockDetailForm(forms.ModelForm):
    class Meta:
        model = PackedStock
        fields = ['quantity']

class RemoveStockForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, label="Quantity to remove")
    confirm = forms.BooleanField(required=False, label="Confirm over-removal")
