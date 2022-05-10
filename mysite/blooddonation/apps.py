from django.apps import AppConfig


class BlooddonationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blooddonation'

    def ready(self):
        try:
            import apps.blooddonation.signals 
        except ImportError:
            pass
