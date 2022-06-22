from django.db import models
from django.urls import reverse

from .utils import render_link_tag


class ModelMixin:
    """A class to represent extra project-wide utilities for models."""

    def render_admin_change_link(self, content=None, model_admin=None, **attrs):
        return render_link_tag(
            reverse(
                "{}:{}_{}_change".format(
                    model_admin.admin_site.name if model_admin else "admin",
                    self._meta.app_label,
                    self._meta.model_name,
                ),
                args=(self.id,),
            ),
            content or str(self),
            **attrs,
        )


class NamedModel(models.Model):
    """A class to represent an abstract model with name and abbreviation fields."""

    name = models.CharField("nazwa", max_length=100)
    abbreviation = models.CharField("skrót", max_length=20)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name or self.abbreviation
