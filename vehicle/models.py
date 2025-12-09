from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
from django.conf import settings 
from .enums import VehicleStatus

User = settings.AUTH_USER_MODEL 

# -----------------------------
# Vehicle Model
# -----------------------------
class Vehicle(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=VehicleStatus.choices,
        default=VehicleStatus.AVAILABLE
    )
    dealer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='vehicles'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.make} {self.model})"



