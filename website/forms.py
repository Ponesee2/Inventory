from django import forms
from .models import *


class SupplierForm(forms.ModelForm):
    class Meta: 
        model = Supplier
        fields = ['name', 'contact_person', 'number', 'location']
        widgets = {
            'name' : forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder' : 'Input Name'
            }),
            'contact_person' : forms.TextInput(attrs={
                'class' :  'form-control',
                'placeholder' : 'input Contact Person'
            }),
            'number' : forms.NumberInput(attrs={
                'class' : 'form-control',
                'placeholder': 'Input Contact Number'
            }),
            'location' : forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder' :  'Input Location'
            })
            
        }

class InventoryItemForm(forms.ModelForm):
    class Meta:
        
        fields = ['name', 'quantity', 'price']