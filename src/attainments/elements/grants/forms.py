from ..forms import AttainmentAdminForm
from .models import Grant


class GrantAdminForm(AttainmentAdminForm):
    """A class to represent admin change form of the Grant model."""

    class Meta(AttainmentAdminForm.Meta):
        model = Grant
