from django.db import models

class AuctionStatus(models.TextChoices):
    SCHEDULED = 'SCHEDULED', 'Scheduled'
    ACTIVE = 'ACTIVE', 'Active'
    FINISHED = 'FINISHED', 'Finished'
    CANCELLED = 'CANCELLED', 'Cancelled'
