from django.contrib import admin
from django.utils.text import capfirst

from .forms import ContributionAdminForm
from .models import Author, Contribution, ContributionStatus


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Admin options for the Author model."""

    fieldsets = [
        (None, {"fields": ["id"]}),
        ("Informacje podstawowe", {"fields": ["employee", "alias"]}),
    ]
    readonly_fields = ["id"]
    autocomplete_fields = ["employee"]

    list_display = ["id", "employee", "alias"]
    search_fields = [
        "employee__user__last_name",
        "employee__user__first_name",
        "alias",
    ]


@admin.register(Contribution)
class ContributionAdmin(admin.ModelAdmin):
    """Admin options for the Contribution model."""

    form = ContributionAdminForm

    fieldsets = [
        (None, {"fields": ["id"]}),
        (
            "Powiązany obiekt",
            {
                "fields": [
                    "content_type",
                    "object_id",
                    "object_preview",
                ]
            },
        ),
        (
            "Informacje dodatkowe",
            {
                "fields": [
                    "author",
                    "order",
                    "percentage",
                    "status",
                    "affiliation",
                ]
            },
        ),
    ]
    readonly_fields = ["id"]
    autocomplete_fields = ["author", "status", "affiliation"]
    radio_fields = {"content_type": admin.VERTICAL}
    list_display = [
        "id",
        "author",
        "content_type__name",
        "object_id",
        "order",
        "percentage",
        "by_employee",
        "status__abbreviation",
        "affiliation__abbreviation",
    ]
    search_fields = ["author__alias"]

    @admin.display(description="Pracownik", boolean=True)
    def by_employee(self, obj):
        return obj.by_employee()

    @admin.display(
        description=capfirst(Contribution._meta.get_field("content_type").verbose_name)
    )
    def content_type__name(self, obj):
        return obj.content_type.name

    @admin.display(
        description=capfirst(Contribution._meta.get_field("status").verbose_name),
        ordering="status__abbreviation",
    )
    def status__abbreviation(self, obj):
        if obj.status:
            return obj.status.abbreviation

    @admin.display(
        description=capfirst(Contribution._meta.get_field("affiliation").verbose_name),
        ordering=[
            "affiliation__faculty__university__abbreviation",
            "affiliation__faculty__abbreviation",
            "affiliation__abbreviation",
        ],
    )
    def affiliation__abbreviation(self, obj):
        if obj.affiliation:
            return obj.affiliation.abbreviation


@admin.register(ContributionStatus)
class ContributionStatusAdmin(admin.ModelAdmin):
    """Admin options for the ContributionStatus model."""

    fieldsets = [
        (None, {"fields": ["id"]}),
        ("Informacje podstawowe", {"fields": ["name", "abbreviation"]}),
    ]
    readonly_fields = ["id"]

    list_display = ["id", "name", "abbreviation"]
    search_fields = ["id", "name", "abbreviation"]
    ordering = ["id"]
