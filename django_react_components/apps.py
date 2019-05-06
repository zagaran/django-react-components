from django.apps import AppConfig


class DjangoReactComponentsConfig(AppConfig):
    name = 'django_react_components'
    
    def ready(self):
        # Add System checks
        from django_react_components.checks import dependency_checks
