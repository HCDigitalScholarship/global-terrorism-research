# Load settings from system environment.
# This is what Docker wants!
#
# To use this, simply call:
#     python manage.py --settings=gtr.settings_docker

import os
import dj_database_url

from .settings import *

DEBUG = os.environ.get('DEBUG', '').lower() in ['true', '1']

ALLOWED_HOSTS = ['*']

SECRET_KEY = os.environ.get('SECRET_KEY')

DATABASES['default'] = dj_database_url.config(
    default='mysql://gtrp:gtrp@db:3306/gtrp'
)
