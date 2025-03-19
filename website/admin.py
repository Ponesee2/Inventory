from django.contrib import admin
from .models import *

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'available_units', 'status', 'supplier', 'date', 'is_archived')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('product', 'units', 'total_price', 'date')

@admin.register(RestockLog)
class RestockLogAdmin(admin.ModelAdmin):
    list_display = ("product", "quantity_added", "timestamp", "supplier")
    ordering = ("-timestamp",)  # Show latest logs first