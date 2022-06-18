from django.db import models


class NamedModel(models.Model):
    """A class to represent an abstract model with name and abbreviation fields."""

    name = models.CharField("nazwa", max_length=50)
    abbreviation = models.CharField("skrót", max_length=10)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name or self.abbreviation
