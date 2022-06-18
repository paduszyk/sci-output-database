from ..models import Attainment


class Grant(Attainment):
    """A class to represent Grant objects."""

    class Meta(Attainment.Meta):
        verbose_name = "grant"
        verbose_name_plural = "granty"
