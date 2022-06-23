from django.db import models

from ..models import Element


class Journal(models.Model):
    """A class to represent the Journal objects."""

    title = models.CharField(verbose_name="tytuł", max_length=255)
    abbreviation = models.CharField(verbose_name="skrót", max_length=255)
    impact_factor = models.DecimalField(
        verbose_name="IF",
        max_digits=6,
        decimal_places=3,
        blank=True,
        null=True,
    )
    points = models.PositiveSmallIntegerField(
        verbose_name="punkty",
        blank=True,
        null=True,
    )
    ancestor = models.ForeignKey(
        to="self",
        on_delete=models.SET_NULL,
        verbose_name="poprzednik",
        related_name="successors",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "czasopismo"
        verbose_name_plural = "czasopisma"

    def __str__(self):
        return self.title


class Article(Element):
    """A class to represent Article objects."""

    journal = models.ForeignKey(
        Journal,
        on_delete=models.CASCADE,
        verbose_name=Journal._meta.verbose_name,
        related_name="articles",
    )
    year = models.PositiveSmallIntegerField("rok")
    volume = models.CharField("wolumin", max_length=255, blank=True)
    pages = models.CharField("strony", max_length=255, blank=True)
    doi = models.CharField("DOI", max_length=255, blank=True)
    impact_factor = models.DecimalField(
        "IF",
        max_digits=6,
        decimal_places=3,
        blank=True,
        null=True,
        editable=False,
    )
    points = models.PositiveSmallIntegerField(
        "punkty",
        blank=True,
        null=True,
        editable=False,
    )

    locked = models.BooleanField("zablokowany", default=False)

    class Meta(Element.Meta):
        verbose_name = "artykuł"
        verbose_name_plural = "artykuły"

    def clean(self):
        if hasattr(self, "journal") and not self.locked:
            self.impact_factor, self.points = (
                self.journal.impact_factor,
                self.journal.points,
            )
