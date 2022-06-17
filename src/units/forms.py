from django import forms
from django.utils.text import capfirst

from .models import Department, University
from .widgets import ReadOnlyInput


class ReadOnlyField(forms.CharField):
    """A class representing a field for showing read-only data in forms."""

    def __init__(self, **kwargs):
        kwargs.update(
            {
                "required": False,
                "max_length": 255,
                "widget": ReadOnlyInput(),
            }
        )
        super().__init__(**kwargs)


class DepartmentAdminForm(forms.ModelForm):
    """A class to represent admin change form of the Department model."""

    class Meta:
        model = Department
        fields = "__all__"

    university = ReadOnlyField(label=capfirst(University._meta.verbose_name))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            self.fields["university"].initial = getattr(
                self.instance.faculty, "university"
            )
