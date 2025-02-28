from django.db import models

class Supplier(models.Model):
    name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100)
    number = models.CharField(max_length=20)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    