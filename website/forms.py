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

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product  # Fixed typo (changed 'models' to 'model')
        fields = ['name', 'price', 'supplier', 'units', 'available_units', 'status', 'date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Input Name'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Input Price'}),
            'supplier': forms.Select(attrs={'class': 'form-control'}),
            'units' : forms.NumberInput(attrs={'class': 'form-control'}),
            'available_units': forms.NumberInput(attrs={'class':'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
        }

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['product', 'units']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'units' : forms.NumberInput(attrs={'Class': 'form-control'})
        }
