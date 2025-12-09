from django.db import models
from django.utils import timezone
from users.models import User
from vehicle.models import Vehicle
from .enums import AuctionStatus


class Auction(models.Model):
    # Relations
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name='auctions'
    )
    dealer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='auctions'
    )

    # Auction fields
    start_price = models.DecimalField(max_digits=12, decimal_places=2)
    current_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=AuctionStatus.choices,
        default=AuctionStatus.SCHEDULED
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Auction"
        verbose_name_plural = "Auctions"

    def __str__(self):
        return f"Auction {self.id} - {self.vehicle.title} ({self.status})"

    def save(self, *args, **kwargs):
        # Set current_price to start_price initially if not provided
        if self.current_price is None:
            self.current_price = self.start_price
        super().save(*args, **kwargs)

    @property
    def is_active(self):
        now = timezone.now()
        return self.start_time <= now <= self.end_time and self.status == AuctionStatus.ACTIVE
