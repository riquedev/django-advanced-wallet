import os
from django.apps import AppConfig


class TestsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = os.environ.get('DJANGO_EXAMPLE_APP', "example_app.tests")
