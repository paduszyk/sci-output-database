from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Employee, Employment


@receiver(post_save, sender=Employee)
def create_employment(sender, instance, created, **kwargs):
    """Create Employment object related to the newly added sender Employee instance."""
    if created or not hasattr(instance, "employment"):
        Employment.objects.create(employee=instance)
