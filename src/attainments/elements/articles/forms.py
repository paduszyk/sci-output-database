from extras.forms import ReadOnlyField

from ..forms import ElementAdminForm
from .models import Article


class ArticleAdminForm(ElementAdminForm):
    """A class to represent admin change form of the Article model."""

    class Meta:
        model = Article
        fields = "__all__"

    impact_factor_ = ReadOnlyField(label="IF")
    points_ = ReadOnlyField(label="Punkty")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            self.fields["impact_factor_"].initial, self.fields["points_"].initial = (
                self.instance.impact_factor or "-",
                self.instance.points or "-",
            )
