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

    def get_fieldsets(self, request, obj):
        fieldsets = list(super().get_fieldsets(request, obj))
        if obj:
            fieldsets = [
                (None, {"fields": ["id"]}),
                ("Informacje podstawowe", fieldsets[0][1]),
                *fieldsets[1:],
            ]
        return fieldsets

    def get_readonly_fields(self, request, obj):
        return ["id", *list(super().get_readonly_fields(request, obj))]

    def get_list_display(self, request):
        return ["id", *list(super().get_list_display(request))]

    def get_list_filter(self, request):
        return ()

    def get_ordering(self, request):
        return ["last_name", "first_name", "id"]
