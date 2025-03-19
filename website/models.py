from django.db import models
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from django.db.models import Sum
from datetime import timedelta


class Supplier(models.Model):
    name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100)
    number = models.CharField(max_length=20)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Product(models.Model): 
    class StatusChoices(models.TextChoices):
        AVAILABLE = 'Available', 'Available'
        OUT_OF_STOCK = 'Out of Stock', 'Out of Stock'
        UNAVAILABLE = 'Unavailable', 'Unavailable' 

    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)  
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

    date = models.DateTimeField(default=now)
    is_archived = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        """Automatically update status based on available stock."""
        if self.available_units == 0:
            self.status = self.StatusChoices.OUT_OF_STOCK
        elif self.status == self.StatusChoices.OUT_OF_STOCK and self.available_units > 0:
            self.status = self.StatusChoices.AVAILABLE
        super().save(*args, **kwargs)

    def __str__(self):  
        return self.name

class RestockLog(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_added = models.IntegerField()
    timestamp = models.DateTimeField(default=now)
    supplier = models.ForeignKey(
        'Supplier', 
        on_delete=models.PROTECT, 
        null=True, 
        blank=True
    )

    def __str__(self):
        return f"Restocked {self.quantity_added} units of {self.product.name} on {self.timestamp}"

class Transaction(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    units = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)  
    amount_given = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    change = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=0.00)
    date = models.DateTimeField(default=now)

    def clean(self):
        """Ensure enough stock is available before processing transaction."""
        if self.units > self.product.available_units:
            raise ValidationError(f"Not enough stock for {self.product.name}. Only {self.product.available_units} left.")

    def save(self, *args, **kwargs):
        """Calculate total price, check payment, and update stock."""
        self.total_price = self.units * self.product.price  

        if self.amount_given < self.total_price:
            raise ValidationError("Insufficient payment amount.")

        self.change = self.amount_given - self.total_price  

        # Deduct stock
        self.product.available_units -= self.units  
        self.product.save()  

        super().save(*args, **kwargs)  

    def __str__(self):
        return f"{self.units} units of {self.product.name} - Total: {self.total_price}"


# Reporting Utility Functions
class SalesReport:
    @staticmethod
    def daily_sales():
        return Transaction.objects.filter(date__date=now().date()).aggregate(total=Sum("total_price"))["total"] or 0

    @staticmethod
    def weekly_sales():
        start_of_week = now().date() - timedelta(days=now().weekday())
        return Transaction.objects.filter(date__date__gte=start_of_week).aggregate(total=Sum("total_price"))["total"] or 0

    @staticmethod
    def monthly_sales():
        start_of_month = now().date().replace(day=1)
        return Transaction.objects.filter(date__date__gte=start_of_month).aggregate(total=Sum("total_price"))["total"] or 0
