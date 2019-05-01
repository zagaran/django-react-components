from django.apps import AppConfig


class DjangoReactLoaderConfig(AppConfig):
    name = 'django_react_loader'
    
    def ready(self):
        # Add System checks
        from django_react_loader.checks import dependency_checks
