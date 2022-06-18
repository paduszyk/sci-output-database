from django.contrib import admin

from .forms import ContributionAdminForm
from .models import Author, Contribution


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
        ("Informacje dodatkowe", {"fields": ["author", "order", "percentage"]}),
    ]
    readonly_fields = ["id"]
    autocomplete_fields = ["author"]
    radio_fields = {"content_type": admin.VERTICAL}
    list_display = ["id", "author", "order", "percentage", "by_employee"]
    search_fields = ["author__alias"]

    @admin.display(description="Pracownik", boolean=True)
    def by_employee(self, obj):
        return obj.author.employee is not None
