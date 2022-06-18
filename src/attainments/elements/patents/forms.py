from ..forms import AttainmentAdminForm
from .models import Patent


class PatentAdminForm(AttainmentAdminForm):
    """A class to represent admin change form of the Grant model."""

    class Meta(AttainmentAdminForm.Meta):
        model = Patent
