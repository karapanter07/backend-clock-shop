from django.apps import AppConfig


class AppcommerceConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "Appcommerce"

    def ready(self):
        import Appcommerce.signals