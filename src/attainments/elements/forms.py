from django import forms

from extras.forms import ReadOnlyField


class ElementAdminForm(forms.ModelForm):
    """A class to represent admin change form of the Element model."""

    class Meta:
        fields = "__all__"

    authors = ReadOnlyField(label="Autorzy")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            self.fields["authors"].initial = self.instance.authors_list
            if not self.instance.only_by_employees():
                self.fields[
                    "authors"
                ].help_text = (
                    "Autorów niebędących pracownikami zaznaczono kolorem jasnoszarym."
                )
        else:
            self.fields["authors"].help_text = ""
