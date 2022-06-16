from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    A class to represent User objects.

    Based on Django built-in django.contrib.auth AbstractUser, see:
    https://docs.djangoproject.com/en/4.0/topics/auth/customizing/
    """
