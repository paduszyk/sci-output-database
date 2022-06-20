from ..forms import ElementAdminForm
from .models import Patent


class PatentAdminForm(ElementAdminForm):
    """A class to represent admin change form of the Grant model."""

    class Meta(ElementAdminForm.Meta):
        model = Patent
