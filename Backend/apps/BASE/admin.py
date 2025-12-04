from django.apps import apps
from django.contrib import admin


def register_all_models():
    models = apps.get_models()
    for model in models:
        try:  # noqa
            admin.site.register(model)
        except admin.sites.AlreadyRegistered:
            pass


register_all_models()
