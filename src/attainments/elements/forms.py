from django import forms

from extras.forms import ReadOnlyField


class AttainmentAdminForm(forms.ModelForm):
    class Meta:
        fields = "__all__"

    authors = ReadOnlyField(label="Autorzy")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["authors"].initial = self.instance.authors_list or "-"
