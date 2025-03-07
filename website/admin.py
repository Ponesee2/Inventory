from django.contrib import admin
from .models import Product, Transaction

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'available_units', 'status')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('product', 'units', 'total_price', 'date')
