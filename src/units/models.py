from django.db import models

from extras.models import NamedModel


class Unit(NamedModel):
    """A class to represent abstract Unit objects."""

    class Meta(NamedModel.Meta):
        abstract = True


class University(Unit):
    """A class to represent University objects."""

    class Meta(Unit.Meta):
        verbose_name = "uczelnia"
        verbose_name_plural = "uczelnie"


class Faculty(Unit):
    """A class to represent Faculty objects."""

    university = models.ForeignKey(
        to=University,
        on_delete=models.CASCADE,
        verbose_name=University._meta.verbose_name,
        related_name="faculties",
    )

    class Meta(Unit.Meta):
        verbose_name = "wydział"
        verbose_name_plural = "wydziały"


class Department(Unit):
    """A class to represent Department objects."""

    faculty = models.ForeignKey(
        to=Faculty,
        on_delete=models.CASCADE,
        verbose_name=Faculty._meta.verbose_name,
        related_name="departments",
    )

    class Meta(Unit.Meta):
        verbose_name = "katedra"
        verbose_name_plural = "katedry"
