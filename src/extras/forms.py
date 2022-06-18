from django import forms

from . import widgets


class ReadOnlyField(forms.CharField):
    """A class representing a field for showing read-only data in forms."""

    def __init__(self, **kwargs):
        kwargs.update(
            {
                "required": False,
                "max_length": 255,
                "widget": widgets.ReadOnlyInput(),
            }
        )
        super().__init__(**kwargs)
