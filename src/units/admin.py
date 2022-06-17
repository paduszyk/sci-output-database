from django.contrib import admin

from .models import Department, Faculty, University


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    """Admin options for the University model."""


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    """Admin options for the Faculty model."""


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    """Admin options for the Department model."""
