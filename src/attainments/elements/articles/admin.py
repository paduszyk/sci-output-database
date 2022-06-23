from django.contrib import admin
from django.utils.text import capfirst

from ..admin import ElementAdmin
from .forms import ArticleAdminForm
from .models import Article, Journal


@admin.register(Article)
class ArticleAdmin(ElementAdmin):
    """Admin options for the Article model."""

    form = ArticleAdminForm

    fieldsets = [
        ("Wydawnictwo", {"fields": ["journal", "year", "volume", "pages", "doi"]}),
        ("Ewaluacja", {"fields": ["impact_factor_", "points_"]}),
        ("Informacje dodatkowe", {"fields": ["locked"]}),
    ]
    autocomplete_fields = ["journal"]

    list_display = ["year", "journal__abbreviation", "volume", "pages", "locked"]

    @admin.display(
        description=capfirst(Article._meta.get_field("journal").verbose_name),
        ordering="journal__abbreviation",
    )
    def journal__abbreviation(self, obj):
        return obj.journal.abbreviation


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
