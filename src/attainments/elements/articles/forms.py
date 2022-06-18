from ..forms import AttainmentAdminForm
from .models import Article


class ArticleAdminForm(AttainmentAdminForm):
    """A class to represent admin change form of the Article model."""

    class Meta(AttainmentAdminForm.Meta):
        model = Article
