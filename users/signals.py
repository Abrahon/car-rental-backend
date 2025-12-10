# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import User 

@receiver(post_save, sender=User)
def send_approval_notification(sender, instance, created, update_fields=None, **kwargs):
    # Only send email when an existing user gets approved
    if (
        not created and 
        instance.is_approved and 
        update_fields and "is_approved" in update_fields
    ):
        send_mail(
            subject="Dealer Approved",
            message="Your account has been approved by the Admin.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.email],
            fail_silently=False,
        )
