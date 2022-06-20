from django.contrib import admin

from ..admin import ElementAdmin
from .forms import GrantAdminForm
from .models import Grant


@admin.register(Grant)
class GrantAdmin(ElementAdmin):
    """Admin options for the Grant model."""

    form = GrantAdminForm
