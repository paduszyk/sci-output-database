from django.contrib import admin

from ..admin import ElementAdmin
from .forms import PatentAdminForm
from .models import Patent


@admin.register(Patent)
class PatentAdmin(ElementAdmin):
    """Admin options for the Patent model."""

    form = PatentAdminForm
