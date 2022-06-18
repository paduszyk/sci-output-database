from django.contrib import admin

from ..admin import AttainmentAdmin
from .forms import PatentAdminForm
from .models import Patent


@admin.register(Patent)
class PatentAdmin(AttainmentAdmin):
    """Admin options for the Patent model."""

    form = PatentAdminForm
