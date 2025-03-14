from django.apps import AppConfig as AC # to fix a mypy error


class AppConfig(AC):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
