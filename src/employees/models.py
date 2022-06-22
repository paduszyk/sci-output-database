from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models

from extras.models import NamedModel
from units.models import Department

User = get_user_model()


class Status(NamedModel):
    """A class to represent the Status objects."""

    class Meta:
        verbose_name = "status"
        verbose_name_plural = "statusy"


class Degree(NamedModel):
    """A class to represent the Degree objects."""

    abbreviation = None

    class Meta:
        verbose_name = "tytuł/stopień"
        verbose_name_plural = "tytuły i stopnie"


class Domain(NamedModel):
    """A class to represent the Domain objects."""

    class Meta:
        verbose_name = "dziedzina"
        verbose_name_plural = "dziedziny"


class Discipline(NamedModel):
    """A class to represent Discipline objects."""

    domain = models.ForeignKey(
        to=Domain,
        on_delete=models.CASCADE,
        verbose_name=Domain._meta.verbose_name,
        related_name="disciplines",
    )

    class Meta:
        verbose_name = "dyscyplina"
        verbose_name_plural = "dyscypliny"


class Group(NamedModel):
    """A class to represent the Group objects."""

    class Meta:
        verbose_name = "grupa"
        verbose_name_plural = "grupy"


class Subgroup(NamedModel):
    """A class to represent the Subgroup objects."""

    group = models.ForeignKey(
        to=Group,
        on_delete=models.CASCADE,
        verbose_name=Group._meta.verbose_name,
        related_name="subgroups",
    )

    class Meta:
        verbose_name = "podgrupa"
        verbose_name_plural = "podgrupy"


class Position(NamedModel):
    """A class to represent the Position objects."""

    abbreviation = None
    subgroups = models.ManyToManyField(
        to=Subgroup,
        verbose_name=Subgroup._meta.verbose_name_plural,
        blank=True,
    )

    class Meta:
        verbose_name = "stanowisko"
        verbose_name_plural = "stanowiska"

    def has_valid_subgroups(self):
        subgroup_ids = self.subgroups.all().values_list("group", flat=True)
        return len(list(set(subgroup_ids))) == 1

    @property
    def group(self):
        if self.has_valid_subgroups():
            return self.subgroups.first().group


class Employee(models.Model):
    """A class to represent the Employee objects."""

    class SexChoices(models.TextChoices):
        FEMALE = "F", "kobieta"
        MALE = "M", "mężczyzna"

    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        verbose_name=User._meta.verbose_name,
    )
    sex = models.CharField(
        verbose_name="płeć",
        max_length=1,
        choices=SexChoices.choices,
        default=SexChoices.FEMALE,
    )
    degree = models.ForeignKey(
        to=Degree,
        on_delete=models.SET_NULL,
        verbose_name=Degree._meta.verbose_name,
        related_name="employees",
        blank=True,
        null=True,
    )
    status = models.ForeignKey(
        to=Status,
        on_delete=models.SET_NULL,
        verbose_name=Status._meta.verbose_name,
        related_name="employees",
        blank=True,
        null=True,
    )
    in_evaluation = models.BooleanField(
        verbose_name="w liczbie N",
        choices=[(True, "Tak"), (False, "Nie")],
        default=True,
    )
    discipline = models.ForeignKey(
        to=Discipline,
        on_delete=models.SET_NULL,
        verbose_name=Discipline._meta.verbose_name,
        related_name="employees",
        blank=True,
        null=True,
    )
    orcid = models.CharField(
        verbose_name="ORCID",
        max_length=19,
        unique=True,
        blank=True,
        null=True,
        default=None,
        validators=[RegexValidator(r"^\d{4}-\d{4}-\d{4}-\d{3}(\d|X)$")],
    )

    class Meta:
        verbose_name = "pracownik"
        verbose_name_plural = "pracownicy"

    def __str__(self):
        return "{}{}".format(
            self.user.get_short_name(),
            f", {self.degree}" if self.degree else "",
        )

    @property
    def last_name(self):
        return self.user.last_name

    @property
    def first_name(self):
        return self.user.first_name

    @property
    def email(self):
        return self.user.email


class Employment(models.Model):
    """A class to represent the Employment objects."""

    employee = models.OneToOneField(
        to=Employee,
        on_delete=models.CASCADE,
        verbose_name=Employee._meta.verbose_name,
    )
    position = models.ForeignKey(
        Position,
        on_delete=models.SET_NULL,
        verbose_name=Position._meta.verbose_name,
        related_name="employments",
        blank=True,
        null=True,
    )
    subgroup = models.ForeignKey(
        Subgroup,
        on_delete=models.SET_NULL,
        verbose_name=Subgroup._meta.verbose_name,
        related_name="employments",
        blank=True,
        null=True,
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        verbose_name=Department._meta.verbose_name,
        related_name="employments",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "zatrudnienie"
        verbose_name_plural = "zatrudnienia"

    def __str__(self):
        return "{} {}".format(
            str(self.employee),
            f"({', '.join(employment_info.values())})"
            if (
                employment_info := {
                    key: value
                    for key, field in [
                        ("position", "name"),
                        ("subgroup", "abbreviation"),
                        ("department", "abbreviation"),
                    ]
                    if (value := getattr(getattr(self, key), field, None))
                }
            )
            else "",
        ).strip()
