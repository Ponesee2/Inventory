from django.db import models
from django.utils.timezone import now

class Supplier(models.Model):
    name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100)
    number = models.CharField(max_length=20)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name

from django.db import models
from django.utils.timezone import now
from django.core.exceptions import ValidationError

class Product(models.Model): 
    class StatusChoices(models.TextChoices):
        AVAILABLE = 'Available', 'Available'
        ASSIGNED = 'Assigned', 'Assigned'
        MAINTENANCE = 'Maintenance', 'Maintenance'
        DISPOSED = 'Disposed', 'Disposed'
        LOST = 'Lost', 'Lost'
        STOLEN = 'Stolen', 'Stolen'

    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Changed to DecimalField
    units = models.IntegerField()
    available_units = models.IntegerField()
        
    status = models.CharField( 
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.AVAILABLE
    )

    supplier = models.ForeignKey(
        'Supplier', 
        on_delete=models.PROTECT, 
        null=True, 
        blank=True
    )

    date = models.DateTimeField(default=now, blank=False, null=False)
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, null=True, blank=True)
    units = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)  # Auto-calculated
    date = models.DateTimeField(default=now, blank=False, null=False)

    def clean(self):
        """Ensure enough stock is available before processing transaction."""
        if self.product and self.units > self.product.available_units:
            raise ValidationError(f"Not enough stock available for {self.product.name}. Only {self.product.available_units} units left.")

    def save(self, *args, **kwargs):
        """Calculate total price and update product's available stock."""
        if self.product:
            self.total_price = self.units * self.product.price  # Calculate total price
            self.product.available_units -= self.units  # Deduct sold units
            self.product.save()  # Save changes to Product

        super().save(*args, **kwargs)  # Save the transaction

    def __str__(self):
        return f"{self.units} units of {self.product.name} - Total: {self.total_price}"
