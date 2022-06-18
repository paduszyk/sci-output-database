from django import forms
from django.utils.text import capfirst

from extras.forms import ReadOnlyField

from .models import Department, University


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
