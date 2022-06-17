from django.contrib import admin

from .models import Department, Faculty, University


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    """Admin options for the University model."""

    class FacultyInLine(admin.TabularInline):
        model = Faculty
        extra = 0

    fieldsets = [
        (None, {"fields": ["id"]}),
        ("Informacje podstawowe", {"fields": ["name", "abbreviation"]}),
    ]
    readonly_fields = ["id"]
    inlines = [FacultyInLine]

    list_display = ["id", "name", "abbreviation"]
    search_fields = ["name", "abbreviation"]


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    """Admin options for the Faculty model."""

    class DepartmentInLine(admin.TabularInline):
        model = Department
        extra = 0

    fieldsets = [
        (None, {"fields": ["id"]}),
        ("Informacje podstawowe", {"fields": ["name", "abbreviation"]}),
        ("Jednostka nadrzędna", {"fields": ["university"]}),
    ]
    readonly_fields = ["id"]
    autocomplete_fields = ["university"]
    inlines = [DepartmentInLine]

    list_display = ["id", "name", "abbreviation", "university__name"]
    search_fields = ["name", "abbreviation", "university__name"]

    @admin.display(
        description=Faculty._meta.get_field("university").verbose_name,
        ordering="university__name",
    )
    def university__name(self, obj):
        return obj.university.name


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    """Admin options for the Department model."""

    fieldsets = [
        (None, {"fields": ["id"]}),
        ("Informacje podstawowe", {"fields": ["name", "abbreviation"]}),
        ("Jednostka nadrzędna", {"fields": ["faculty"]}),
    ]
    readonly_fields = ["id"]
    autocomplete_fields = ["faculty"]

    list_display = [
        "id",
        "name",
        "abbreviation",
        "faculty__name",
        "faculty__university__name",
    ]
    search_fields = ["name", "abbreviation", "university__name"]

    @admin.display(
        description=Department._meta.get_field("faculty").verbose_name,
        ordering="faculty__name",
    )
    def faculty__name(self, obj):
        return obj.faculty.name

    @admin.display(
        description=Faculty._meta.get_field("university").verbose_name,
        ordering="faculty__university__name",
    )
    def faculty__university__name(self, obj):
        return obj.faculty.university.name
