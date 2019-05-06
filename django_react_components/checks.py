"""
Django System Checks
"""
from django.conf import settings
from django.core.checks import Error, Tags, register


@register(Tags.compatibility)
def dependency_checks(app_configs, **kwargs):
    """
    System check for required dependencies.
    """
    errors = []
    try:
        import webpack_loader
        if 'webpack_loader' not in settings.INSTALLED_APPS:
            errors.append(
                Error(
                    '`django-react-components` requires `django-webpack-loader` to be installed.',
                    hint='Add `webpack_loader` to `settings.INSTALLED_APPS`.',
                    id='drl.E002',
                )
            )
    except ImportError:
        errors.append(
            Error(
                '`django-react-components` requires `django-webpack-loader` to be installed.',
                hint='Please install `django-webpack-loader`.',
                id='drl.E001',
            )
        )
    return errors
