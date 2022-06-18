from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.text import Truncator

from ..contributions.models import Contribution


class Attainment(models.Model):
    """A class to represent abstract Attainment objects."""

    title = models.TextField(verbose_name="tytuł")
    contributions = GenericRelation(to=Contribution)
    authors_list = models.TextField(verbose_name="Autorzy", editable=False, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return "{} {}".format(
            f"{self.authors_list}:" if self.authors_list else "",
            f"{self.get_truncated_title()}",
        ).strip()

    def get_truncated_title(self, num_words=10):
        return Truncator(self.title).words(num=num_words)

    def get_authors_list(self, separator=";"):
        separator = separator.strip() + " "
        return separator.join(
            contribution.author.alias
            for contribution in self.contributions.all().order_by("order")
        )
