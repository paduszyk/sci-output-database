from ..forms import ElementAdminForm
from .models import Article


class ArticleAdminForm(ElementAdminForm):
    """A class to represent admin change form of the Article model."""

    class Meta(ElementAdminForm.Meta):
        model = Article
