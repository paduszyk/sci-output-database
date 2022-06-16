from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.models import Group

from .models import User

# Grouping users is not relevant for the project, hence the built-in
# auth.Group model it is unregistered from the admin site.

admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(AuthUserAdmin, admin.ModelAdmin):
    """Admin options for the User model."""
