from django.db import models
from django.conf import settings 
from vehicle.models import Vehicle
User = settings.AUTH_USER_MODEL 



class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    vehicle = models.OneToOneField(
        Vehicle, 
        on_delete=models.CASCADE,
        related_name='order'
    )
    price = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} - {self.vehicle.title} by {self.user.email}"