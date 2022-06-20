from ..models import Element


class Grant(Element):
    """A class to represent Grant objects."""

    class Meta(Element.Meta):
        verbose_name = "grant"
        verbose_name_plural = "granty"
