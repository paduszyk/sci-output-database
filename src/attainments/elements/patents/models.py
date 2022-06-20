from ..models import Element


class Patent(Element):
    """A class to represent Patent objects."""

    class Meta(Element.Meta):
        verbose_name = "patent"
        verbose_name_plural = "patenty"
