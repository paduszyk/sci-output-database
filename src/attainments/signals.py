from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .contributions.models import Contribution
from .elements.models import Element


@receiver([post_save, post_delete], sender=Contribution)
def update_element_authors_list(sender, instance, **kwargs):
    """
    A signal for updating `authors_list` attribute of Element-based models.
    """
    element_class = instance.content_type.model_class()
    if element_class not in Element.__subclasses__():
        raise TypeError(
            f"{element_class.__module__}.{element_class.__name__} has to "
            f"inherit from {Element.__module__}.{Element.__name__}"
        )

    try:
        obj = element_class.objects.get(pk=instance.object_id)
    except element_class.DoesNotExist:
        return
    obj.authors_list = obj.get_authors_list()

    obj.save()
