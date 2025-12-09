from django.db import models

class VehicleStatus(models.TextChoices):
    PENDING_APPROVAL = 'PENDING_APPROVAL', 'Pending Approval'  
    AVAILABLE = 'AVAILABLE', 'Available'
    SOLD = 'SOLD', 'Sold'
