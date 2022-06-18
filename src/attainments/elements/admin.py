from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.utils.html import format_html

from ..contributions.models import Contribution


class ContributionInline(GenericTabularInline):
    model = Contribution
    extra = 0
    autocomplete_fields = ["author"]


class AttainmentAdmin(admin.ModelAdmin):
    """Admin options for the Attainment model."""

    def get_fieldsets(self, request, obj):
        return [
            (None, {"fields": ["id"]}),
            ("Dane podstawowe", {"fields": ["title", "authors"]}),
        ] + list(self.fieldsets or ())

    def get_readonly_fields(self, request, obj):
        return ["id"]

    def get_inlines(self, request, obj):
        inlines = super().get_inlines(request, obj)
        if ContributionInline in inlines:
            inlines.remove(ContributionInline)
        return [ContributionInline] + inlines

    def get_list_display(self, request):
        if self.list_display == ("__str__",):
            self.list_display = []
        return ["id", "authors_list", "title_html"] + list(self.list_display)

    @admin.display(description="Tytuł", ordering="title")
    def title_html(self, obj):
        return format_html(obj.title)
