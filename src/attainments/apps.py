from django.apps import AppConfig


class AttainmentsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "attainments"
    verbose_name = "Dorobek"

    def ready(self):
        from . import signals
