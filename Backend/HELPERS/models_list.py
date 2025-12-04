from django.conf import settings

def get_installed_apps():
    return settings.INSTALLED_APPS

print(get_installed_apps())
