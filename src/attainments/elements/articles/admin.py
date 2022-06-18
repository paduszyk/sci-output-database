from django.contrib import admin

from ..admin import AttainmentAdmin
from .forms import ArticleAdminForm
from .models import Article


@admin.register(Article)
class ArticleAdmin(AttainmentAdmin):
    """Admin options for the Article model."""

    form = ArticleAdminForm
