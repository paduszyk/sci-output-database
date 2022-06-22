from django.contrib import admin

from ..admin import ElementAdmin
from .forms import ArticleAdminForm
from .models import Article, Journal


@admin.register(Article)
class ArticleAdmin(ElementAdmin):
    """Admin options for the Article model."""

    form = ArticleAdminForm


@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    """Admin options for the Journal model."""

    fieldsets = (
        (None, {"fields": ["id"]}),
        ("Informacje podstawowe", {"fields": ["title", "abbreviation"]}),
        ("Ewaluacja", {"fields": ["impact_factor", "points"]}),
        ("Dane dodatkowe", {"fields": ["ancestor"]}),
    )
    readonly_fields = ["id"]
    autocomplete_fields = ["ancestor"]

    list_display = [
        "id",
        "title",
        "abbreviation",
        "impact_factor",
        "points",
        "ancestor__title",
        "successors__title",
    ]
    search_fields = [
        "title",
        "abbr",
        "ancestor__title",
        "ancestor__abbr",
        "successors__title",
        "successors__abbr",
    ]

    @admin.display(description="Poprzednik", ordering="ancestor__title")
    def ancestor__title(self, obj):
        if obj.ancestor:
            return obj.ancestor.title

    @admin.display(description="Następcy")
    def successors__title(self, obj):
        if obj.successors:
            return ", ".join(obj.successors.all().values_list("title", flat=True))
