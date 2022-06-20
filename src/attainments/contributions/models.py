from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from employees.models import Employee
from extras.models import ModelMixin, NamedModel
from units.models import Department


class Author(ModelMixin, models.Model):
    """A class to represent Author objects."""

    employee = models.ForeignKey(
        to=Employee,
        on_delete=models.SET_NULL,
        verbose_name=Employee._meta.verbose_name,
        blank=True,
        null=True,
    )
    alias = models.CharField(verbose_name="alias", max_length=50, blank=True)

    class Meta:
        verbose_name = "autor"
        verbose_name_plural = "autorzy"
        constraints = [
            models.UniqueConstraint(
                fields=["alias", "employee"],
                name="unique_author_alias_employee",
            )
        ]

    def __str__(self):
        if self.is_employed():
            return str(self.employee.employment)
        if self.is_employee():
            return str(self.employee)
        return self.alias

    def clean(self):
        if not (self.employee or self.alias):
            raise ValidationError(
                "Utworzenie/zmiana autora wymaga podania aliasu "
                "lub wskazania pracownika."
            )
        if self.employee and not self.alias:
            self.alias = self.employee.user.get_short_name()

    def is_employee(self):
        return self.employee is not None

    def is_employed(self):
        return self.employee and hasattr(self.employee, "employment")

    @property
    def department(self):
        if self.is_employed():
            return self.employee.employment.department


class ContributionStatus(NamedModel):
    """A class to represent ContributionStatus objects."""

    class Meta:
        verbose_name = "status udziału"
        verbose_name_plural = "statusy udziałów"


class Contribution(models.Model):
    """A class to represent AbstractContribution objects."""

    content_type = models.ForeignKey(
        to=ContentType,
        on_delete=models.CASCADE,
        verbose_name="rodzaj elementu",
        related_name="contributions",
    )
    object_id = models.PositiveIntegerField(verbose_name="ID elementu")
    content_object = GenericForeignKey(ct_field="content_type", fk_field="object_id")
    order = models.PositiveIntegerField(
        verbose_name="numer",
        validators=[MinValueValidator(1)],
        default=1,
    )
    author = models.ForeignKey(
        to=Author,
        on_delete=models.CASCADE,
        verbose_name=Author._meta.verbose_name,
        related_name="contributions",
    )
    percentage = models.PositiveSmallIntegerField(
        verbose_name="udział (%)",
        validators=[MaxValueValidator(100)],
        default=0,
    )
    status = models.ForeignKey(
        to=ContributionStatus,
        on_delete=models.SET_NULL,
        verbose_name="status",
        related_name="contributions",
        blank=True,
        null=True,
    )
    affiliation = models.ForeignKey(
        to=Department,
        on_delete=models.SET_NULL,
        verbose_name="afiliacja",
        related_name="contributions",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "udział"
        verbose_name_plural = "udziały"

    def __str__(self):
        return (
            f"{self.author}, w elemencie typu "
            f"{self.content_type.model_class()._meta.verbose_name} "
            f"(ID={self.object_id})"
        )

    def by_employee(self):
        return self.author.employee is not None
