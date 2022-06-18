from django.forms import widgets


class ReadOnlyInput(widgets.Widget):
    """A class to represent a widget for displaying form data as a plain text."""

    template_name = "extras/forms/widgets/read_only_input.html"
