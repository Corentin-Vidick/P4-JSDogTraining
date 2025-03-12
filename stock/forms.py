from django import forms
from .models import PackedStock, LabelStock, Product

class PackedStockForm(forms.ModelForm):
    quantity = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    expiry_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    batch = forms.CharField(required=False, max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = PackedStock
        fields = ['quantity', 'expiry_date', 'batch']

class RemoveStockForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    confirm = forms.BooleanField(required=True, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

class AddStockDetailForm(forms.ModelForm):
    class Meta:
        model = PackedStock
        fields = ['quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        }

class AddLabelStockForm(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=Product.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    quantity = forms.IntegerField(min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = LabelStock
        fields = ['product', 'quantity']
