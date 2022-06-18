from django.contrib import admin

from ..admin import AttainmentAdmin
from .forms import GrantAdminForm
from .models import Grant


@admin.register(Grant)
class GrantAdmin(AttainmentAdmin):
    """Admin options for the Grant model."""

    form = GrantAdminForm
