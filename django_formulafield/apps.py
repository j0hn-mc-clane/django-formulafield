from django.apps import AppConfig


class DjangoFormulafieldConfig(AppConfig):
    name = "django_formulafield"
    
    def ready(self):
        import django_formulafield.signals