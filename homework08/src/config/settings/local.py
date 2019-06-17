from .base import *

import configparser 

DEBUG = True

INSTALLED_APPS += [
    'django.contrib.postgres',
]

# use package configparser to parse file settings.ini
current_dir = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(current_dir, 'settings.ini')

config = configparser.ConfigParser()

with open(config_path, "r") as config_file:
    config.read_file(config_file)


SECRET_KEY = config['database']['SECRET_KEY']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config['database']['DB_NAME'],
        'USER': config['database']['DB_USER'],
        'PASSWORD': config['database']['DB_PASSWORD'],
        'HOST': config['database']['DB_HOST'],
        'PORT': config['database']['DB_PORT'],
    }
}

# 'django.core.mail.backends.smtp.EmailBackend' is not working?
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
SERVER_EMAIL = config['email']['SERVER_EMAIL']
EMAIL_HOST_USER = config['email']['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = config['email']['EMAIL_HOST_PASSWORD']

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
