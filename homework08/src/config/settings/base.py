import os
from decouple import config


def root(*dirs):
    base_dir = os.path.join(os.path.dirname(__file__), '..', '..')
    return os.path.abspath(os.path.join(base_dir, *dirs))


BASE_DIR = root()

SECRET_KEY = config('SECRET_KEY')

INSTALLED_APPS = [
    # ...
]

MIDDLEWARE = [
    # ...
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    # ...
]

WSGI_APPLICATION = 'config.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    # ...
]

STATIC_URL = '/static/'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True