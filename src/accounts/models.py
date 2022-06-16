from django.contrib.auth.models import AbstractUser
from django.utils.text import capfirst


class User(AbstractUser):
    """
    A class to represent User objects.

    Based on Django built-in django.contrib.auth AbstractUser, see:
    https://docs.djangoproject.com/en/4.0/topics/auth/customizing/
    """

    def __str__(self):
        return "{}: {} ({})".format(
            capfirst(self._meta.verbose_name),
            self.get_full_name(),
            self.username,
        )

    def clean(self):
        super().clean()
        self.first_name = capfirst(self.first_name)
        self.last_name = capfirst(self.last_name)

    def get_full_name(self):
        names = self.first_name.split()
        if len(names) > 1:
            for index, name in enumerate(names):
                names[index] = f"{name[:1]}."
        return "{} {}".format(" ".join(names), self.last_name).strip()

    def get_short_name(self):
        names = self.first_name.split()
        return "{} {}".format(
            " ".join([f"{name[0]}." for name in names]),
            self.last_name,
        ).strip()
