from django.db import models
from django.utils.timezone import now

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
        ASSIGNED = 'Assigned', 'Assigned'
        MAINTENANCE = 'Maintenance', 'Maintenance'
        DISPOSED = 'Disposed', 'Disposed'
        LOST = 'Lost', 'Lost'
        STOLEN = 'Stolen', 'Stolen'

    name = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    units = models.IntegerField()
    available_units = models.IntegerField()
        

    status = models.CharField( 
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.AVAILABLE
    )

    supplier = models.ForeignKey(
    Supplier, 
    on_delete=models.PROTECT, 
    null=True, 
    blank=True
    )

    date = models.DateTimeField(default=now, blank=False, null=False)
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return self.name