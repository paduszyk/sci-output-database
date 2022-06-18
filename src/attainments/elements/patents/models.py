from ..models import Attainment


class Patent(Attainment):
    """A class to represent Patent objects."""

    class Meta(Attainment.Meta):
        verbose_name = "patent"
        verbose_name_plural = "patenty"
