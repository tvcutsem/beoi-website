# settings.py for DEVELOPMENT ! 

from settings_common import *
import socket

# Make this unique, and don't share it with anybody. To generate a new one, run this in the python console:
# import string
# from random import choice
# print ''.join([choice(string.letters + string.digits + string.punctuation) for i in range(50)])
SECRET_KEY = '__dummy__'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

