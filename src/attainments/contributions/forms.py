from django import forms
from django.contrib.contenttypes.models import ContentType

from extras.forms import ReadOnlyField

from .models import Contribution


class ContributionAdminForm(forms.ModelForm):
    """A class to represent admin change form of the Contribution model."""

    class Meta:
        model = Contribution
        fields = "__all__"

    class ContentTypeModelChoiceField(forms.ModelChoiceField):
        def label_from_instance(self, obj):
            return obj.name

    content_type = ContentTypeModelChoiceField(
        queryset=ContentType.objects.filter(
            app_label="attainments",
            model__in=["article", "grant", "patent"],
        ),
        label="Rodzaj elementu",
        required=True,
        widget=forms.widgets.RadioSelect(attrs={"class": "radiolist"}),
    )
    object_preview = ReadOnlyField(label="Podgląd obiektu")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["object_preview"].initial = (
            str(self.instance.content_object) if self.instance.pk else "-"
        )
