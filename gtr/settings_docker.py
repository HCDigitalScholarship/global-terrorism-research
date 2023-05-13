# Load settings from system environment.
# This is what Docker wants!
#
# To use this, simply call:
#     python manage.py --settings=gtr.settings_docker

import os

from .settings import *

DEBUG = os.environ.get('DEBUG', '').lower() in ['true', '1']

ALLOWED_HOSTS = ['*']

SECRET_KEY = os.environ.get('SECRET_KEY')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}