from django.contrib import admin

from ..admin import ElementAdmin
from .forms import ArticleAdminForm
from .models import Article


@admin.register(Article)
class ArticleAdmin(ElementAdmin):
    """Admin options for the Article model."""

    form = ArticleAdminForm
