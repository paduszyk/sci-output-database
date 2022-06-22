from django.contrib import admin, messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.html import format_html
from django.utils.text import capfirst

from .forms import EmployeeAdminForm
from .models import (
    Degree,
    Discipline,
    Domain,
    Employee,
    Employment,
    Group,
    Position,
    Status,
    Subgroup,
)


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    """Admin options for the Status model."""

    fieldsets = [
        (None, {"fields": ["id"]}),
        ("Informacje podstawowe", {"fields": ["name", "abbreviation"]}),
    ]
    readonly_fields = ["id"]

    list_display = ["id", "name", "abbreviation"]
    search_fields = ["id", "name", "abbreviation"]
    ordering = ["id"]


@admin.register(Degree)
class DegreeAdmin(admin.ModelAdmin):
    """Admin options for the Degree model."""

    fieldsets = [
        (None, {"fields": ["id"]}),
        ("Informacje podstawowe", {"fields": ["name"]}),
    ]
    readonly_fields = ["id"]

    list_display = ["id", "name"]
    search_fields = ["id", "name"]
    ordering = ["id"]


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    """Admin options for the Domain model."""

    class DisciplineInline(admin.TabularInline):
        model = Discipline
        extra = 0

    fieldsets = [
        (None, {"fields": ["id"]}),
        ("Informacje podstawowe", {"fields": ["name", "abbreviation"]}),
    ]
    readonly_fields = ["id"]
    inlines = [DisciplineInline]

    list_display = ["id", "name", "abbreviation"]
    search_fields = ["id", "name", "abbreviation"]
    ordering = ["id"]


@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    """Admin options for the Discipline model."""

    fieldsets = [
        (None, {"fields": ["id"]}),
        ("Informacje podstawowe", {"fields": ["name", "abbreviation"]}),
        ("Obiekt nadrzędny", {"fields": ["domain"]}),
    ]
    readonly_fields = ["id"]
    autocomplete_fields = ["domain"]

    list_display = ["id", "name", "abbreviation", "domain__name"]
    search_fields = ["id", "name", "abbreviation"]
    ordering = ["id"]

    @admin.display(
        description=capfirst(Discipline._meta.get_field("domain").verbose_name),
        ordering="domain__name",
    )
    def domain__name(self, obj):
        return obj.domain.name


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    """Admin options for the Group model."""

    class SubgroupInline(admin.TabularInline):
        model = Subgroup
        extra = 0

    fieldsets = [
        (None, {"fields": ["id"]}),
        ("Informacje podstawowe", {"fields": ["name", "abbreviation"]}),
    ]
    readonly_fields = ["id"]
    inlines = [SubgroupInline]

    list_display = ["id", "name", "abbreviation"]
    search_fields = ["id", "name", "abbreviation"]
    ordering = ["id"]


@admin.register(Subgroup)
class SubgroupAdmin(admin.ModelAdmin):
    """Admin options for the Subgroup model."""

    fieldsets = [
        (None, {"fields": ["id"]}),
        ("Informacje podstawowe", {"fields": ["name", "abbreviation"]}),
        ("Obiekt nadrzędny", {"fields": ["group"]}),
    ]
    readonly_fields = ["id"]
    autocomplete_fields = ["group"]

    list_display = ["id", "name", "abbreviation", "group__name"]
    search_fields = ["id", "name", "abbreviation"]
    ordering = ["id"]

    @admin.display(
        description=capfirst(Subgroup._meta.get_field("group").verbose_name),
        ordering="group__name",
    )
    def group__name(self, obj):
        return obj.group.name


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    """Admin options for the Position model."""

    fieldsets = [
        (None, {"fields": ["id"]}),
        ("Informacje podstawowe", {"fields": ["name"]}),
        ("Obiekt nadrzędny", {"fields": ["subgroups"]}),
    ]
    readonly_fields = ["id"]
    autocomplete_fields = ["subgroups"]

    list_display = ["id", "name", "group__name", "subgroups__name_list"]
    search_fields = ["id", "name", "abbreviation"]
    ordering = ["id"]

    @admin.display(
        description=capfirst(Position._meta.get_field("subgroups").verbose_name)
    )
    def subgroups__name_list(self, obj):
        return format_html(
            "<br>".join(
                [
                    subgroup.name
                    for subgroup in obj.subgroups.order_by("group__name", "name").all()
                ]
            )
        )

    @admin.display(description=capfirst(Group._meta.verbose_name))
    def group__name(self, obj):
        return obj.group.name


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    """Admin options for the Employee model."""

    class Media:
        css = {"all": ["admin/css/employees/employee/change_form_extras.css"]}

    class EmploymentInline(admin.StackedInline):
        model = Employment
        min_num = 1
        max_num = 1
        autocomplete_fields = ["position", "subgroup", "department"]

    form = EmployeeAdminForm

    fieldsets = [
        (None, {"fields": ["id"]}),
        (
            "Informacje podstawowe",
            {
                "fields": [
                    "user",
                    "first_name",
                    "last_name",
                    "email",
                    "sex",
                    "status",
                    "degree",
                ]
            },
        ),
        ("Ewaluacja", {"fields": ["in_evaluation", "discipline"]}),
        ("Informacje dodatkowe", {"fields": ["orcid"]}),
    ]
    readonly_fields = ["id"]
    autocomplete_fields = ["user", "degree", "status", "discipline"]
    radio_fields = {"sex": admin.HORIZONTAL, "in_evaluation": admin.HORIZONTAL}

    list_display = [
        "id",
        "user__last_name",
        "user__first_name",
        "degree__abbreviation",
        "status__abbreviation",
        "in_evaluation_bool",
        "discipline__domain__abbreviation",
        "discipline__abbreviation",
        "employment__subgroup__group__abbreviation",
        "employment__subgroup__abbreviation",
        "employment__position__name",
        "employment__department__abbreviation",
    ]
    search_fields = [
        "id",
        "user__last_name",
        "user__first_name",
        "user__email",
    ]
    ordering = ["id"]

    def get_inlines(self, request, obj):
        return [__class__.EmploymentInline] if hasattr(obj, "employment") else []

    def response_add(self, request, obj, post_url_continue=None):
        obj_url = '<a href="{}">{}</a>'.format(
            reverse_lazy("admin:employees_employee_change", args=(obj.id,)),
            str(obj),
        )

        self.message_user(
            request,
            message=format_html(
                f"Pracownik &bdquo;{obj_url}&rdquo; został dodany pomyślnie.<br>"
                "Uzupełnij dane na temat zatrudnienia."
            ),
            level=messages.INFO,
        )
        return redirect(
            reverse_lazy(
                "admin:employees_employment_change",
                args=(obj.employment.id,),
            ),
        )

    @admin.display(
        description=capfirst(
            Employee._meta.get_field("user")
            .related_model._meta.get_field("last_name")
            .verbose_name
        ),
        ordering="user__last_name",
    )
    def user__last_name(self, obj):
        return obj.user.last_name

    @admin.display(
        description=capfirst(
            Employee._meta.get_field("user")
            .related_model._meta.get_field("first_name")
            .verbose_name
        ),
        ordering="user__first_name",
    )
    def user__first_name(self, obj):
        return obj.user.first_name

    @admin.display(
        description=capfirst(Employee._meta.get_field("degree").verbose_name),
        ordering="degree__abbreviation",
    )
    def degree__abbreviation(self, obj):
        if obj.degree:
            return obj.degree.abbreviation

    @admin.display(
        description=capfirst(Employee._meta.get_field("status").verbose_name),
        ordering="status__abbreviation",
    )
    def status__abbreviation(self, obj):
        if obj.status:
            return obj.status.abbreviation

    @admin.display(
        description=capfirst(Employee._meta.get_field("in_evaluation").verbose_name),
        boolean=True,
    )
    def in_evaluation_bool(self, obj):
        return obj.in_evaluation

    @admin.display(
        description=capfirst(
            Employee._meta.get_field("discipline")
            .related_model._meta.get_field("domain")
            .verbose_name
        ),
        ordering="discipline__domain__abbreviation",
    )
    def discipline__domain__abbreviation(self, obj):
        if obj.discipline:
            return obj.discipline.domain.abbreviation

    @admin.display(
        description=capfirst(Employee._meta.get_field("discipline").verbose_name),
        ordering="discipline__abbreviation",
    )
    def discipline__abbreviation(self, obj):
        if obj.discipline:
            return obj.discipline.abbreviation

    @admin.display(
        description=capfirst(
            Employee._meta.get_field("employment")
            .related_model._meta.get_field("subgroup")
            .related_model._meta.get_field("group")
            .verbose_name
        ),
        ordering="employment__subgroup__group__abbreviation",
    )
    def employment__subgroup__group__abbreviation(self, obj):
        if obj.employment:
            if obj.employment.subgroup:
                return obj.employment.subgroup.group.abbreviation

    @admin.display(
        description=capfirst(
            Employee._meta.get_field("employment")
            .related_model._meta.get_field("subgroup")
            .verbose_name
        ),
        ordering="employment__subgroup__abbreviation",
    )
    def employment__subgroup__abbreviation(self, obj):
        if obj.employment:
            if obj.employment.subgroup:
                return obj.employment.subgroup.abbreviation

    @admin.display(
        description=capfirst(
            Employee._meta.get_field("employment")
            .related_model._meta.get_field("position")
            .verbose_name
        ),
        ordering="employment__position__name",
    )
    def employment__position__name(self, obj):
        if obj.employment:
            if obj.employment.position:
                return obj.employment.position.name

    @admin.display(
        description=capfirst(
            Employee._meta.get_field("employment")
            .related_model._meta.get_field("department")
            .verbose_name
        ),
        ordering="employment__department__abbreviation",
    )
    def employment__department__abbreviation(self, obj):
        if obj.employment:
            if obj.employment.department:
                return obj.employment.department.abbreviation


@admin.register(Employment)
class EmploymentAdmin(admin.ModelAdmin):
    """Admin options for the Employment model."""

    fieldsets = [
        (None, {"fields": ["id"]}),
        (
            "Informacje podstawowe",
            {
                "fields": [
                    "employee",
                    "subgroup",
                    "position",
                    "department",
                ]
            },
        ),
    ]
    readonly_fields = ["id"]
    autocomplete_fields = ["employee", "subgroup", "position", "department"]

    list_display = [
        "id",
        "employee",
        "subgroup__group__name",
        "subgroup__name",
        "position__name",
        "department__name",
    ]
    search_fields = ["id", "employee__user__last_name", "employee__user__first_name"]
    ordering = ["id"]

    @admin.display(
        description=capfirst(
            Employment._meta.get_field("subgroup")
            .related_model._meta.get_field("group")
            .verbose_name
        ),
        ordering="subgroup__group__name",
    )
    def subgroup__group__name(self, obj):
        if obj.subgroup:
            return obj.subgroup.group.name

    @admin.display(
        description=capfirst(Employment._meta.get_field("subgroup").verbose_name),
        ordering="subgroup__name",
    )
    def subgroup__name(self, obj):
        if obj.subgroup:
            return obj.subgroup.name

    @admin.display(
        description=capfirst(Employment._meta.get_field("position").verbose_name),
        ordering="position__name",
    )
    def position__name(self, obj):
        if obj.position:
            return obj.position.name

    @admin.display(
        description=capfirst(Employment._meta.get_field("department").verbose_name),
        ordering="department__name",
    )
    def department__name(self, obj):
        if obj.department:
            return obj.department.name
