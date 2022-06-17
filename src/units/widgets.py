from django.forms import widgets


class ReadOnlyInput(widgets.Widget):
    """A class representing a widget for displaying form data as a plain text."""

    template_name = "units/widgets/read_only_input.html"
