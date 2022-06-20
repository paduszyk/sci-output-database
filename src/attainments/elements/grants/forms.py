from ..forms import ElementAdminForm
from .models import Grant


class GrantAdminForm(ElementAdminForm):
    """A class to represent admin change form of the Grant model."""

    class Meta(ElementAdminForm.Meta):
        model = Grant
