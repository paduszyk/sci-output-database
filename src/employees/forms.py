from django import forms

from .models import Employee
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


class EmployeeAdminForm(forms.ModelForm):
    """A class to represent admin change form of the Employee model."""

    class Meta:
        model = Employee
        fields = "__all__"

    first_name = ReadOnlyField(label="Imię")
    last_name = ReadOnlyField(label="Nazwisko")
    email = ReadOnlyField(label="E-mail")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            user = self.instance.user

            for field in ["first_name", "last_name", "email"]:
                self.fields[field].initial = getattr(user, field)
