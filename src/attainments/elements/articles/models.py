from ..models import Attainment


class Article(Attainment):
    """A class to represent Article objects."""

    class Meta(Attainment.Meta):
        verbose_name = "artykuł"
        verbose_name_plural = "artykuły"
