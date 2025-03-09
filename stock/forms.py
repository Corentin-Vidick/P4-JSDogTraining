from django import forms
from .models import PackedStock, LabelStock

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

class AddLabelStockForm(forms.ModelForm):
    class Meta:
        model = LabelStock
        fields = ['label_quantity_1', 'label_quantity_2']

    def __init__(self, *args, **kwargs):
        # Pop out the extra parameter "has_two_labels" if provided.
        has_two_labels = kwargs.pop('has_two_labels', False)
        super().__init__(*args, **kwargs)
        if not has_two_labels:
            # Remove the second label quantity field.
            self.fields.pop('label_quantity_2', None)

    def save(self, commit=True):
        instance = super().save(commit=False)
        # If label_quantity_2 isn't in cleaned_data (because we popped it), default it to 0.
        if 'label_quantity_2' not in self.cleaned_data:
            instance.label_quantity_2 = 0
        if commit:
            instance.save()
        return instance
