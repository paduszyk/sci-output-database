from ..models import Element


class Article(Element):
    """A class to represent Article objects."""

    class Meta(Element.Meta):
        verbose_name = "artykuł"
        verbose_name_plural = "artykuły"
