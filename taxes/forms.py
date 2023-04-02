from django import forms
from .models import Entry

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = [
            'title', 
            'description', 
            'memo',
            'user', 
            'total_price', 
            'tax_year',
            'purchase_date', 
            'status', 
            'category',
            'payment_method',
            'receipt_img',
        ]
        # replace field1, field2, field3 with the actual field names from your Entry model