from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .contributions.models import Contribution
from .elements.models import Attainment


@receiver([post_save, post_delete], sender=Contribution)
def update_attainment_authors_list(sender, instance, **kwargs):
    """
    A signal for updating `authors_list` attribute of Attainment-based models.
    """
    Element = instance.content_type.model_class()
    if Element not in Attainment.__subclasses__():
        raise TypeError(
            f"{Element.__module__}.{Element.__name__} has to "
            f"inherit from {Attainment.__module__}.{Attainment.__name__}"
        )

    try:
        obj = Element.objects.get(pk=instance.object_id)
    except Element.DoesNotExist:
        return
    obj.authors_list = obj.get_authors_list()

    obj.save()
