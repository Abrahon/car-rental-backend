
from django.db import models

class RoleChoices(models.TextChoices):
    SUPER_ADMIN = 'ADMIN', 'Admin'
    DEALER = 'DEALER', 'Dealer'
    USER = 'USER', 'User'