from django import forms

from extras.forms import ReadOnlyField

from .models import Employee


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
