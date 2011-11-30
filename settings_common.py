# Django settings for beoi project.
# by default, configured with development settings. For prod, some options have to be overwritten
import os
from datetime import datetime

DEBUG = True
TEMPLATE_DEBUG = DEBUG
# A tuple of IP addresses, as strings, thats see debug comments, when DEBUG is True
INTERNAL_IPS = ("127.0.0.1") 

# email backend for developmt: mails are written to stdout
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
SEND_BROKEN_LINK_EMAILS = True # sent mail warning for 404 errors
EMAIL_SUBJECT_PREFIX = '[beOI Django] '
# You can tell Django to stop reporting particular 404s by tweaking 
# the IGNORABLE_404_ENDS and IGNORABLE_404_STARTS settings

# for error alerts, only for production
ADMINS = (
    ('Damien Leroy', 'damien.leroy@be-oi.be'),
)

# for broken link alerts, only for production
MANAGERS = ADMINS

# The e-mail address that error messages come from, such as those sent to ADMINS and MANAGERS
SERVER_EMAIL = "info@be-oi.be"

TIME_ZONE = 'Europe/Brussels'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
ugettext = lambda s: s
LANGUAGE_CODE = 'fr' # do not change! related to language detection popup
LANGUAGES = (
  ('fr', ugettext('French')),
  ('nl', ugettext('Dutch')),
)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

REGISTRATION_DEADLINE = datetime(2012,01,30,00,00,00)

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '__dummy__' # to be overwritten in settings.py

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
	'django.template.loaders.filesystem.Loader',
	'django.template.loaders.app_directories.Loader',
	#'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
	'django.middleware.common.CommonMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
#	'django.middleware.locale.LocaleMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'beoi.core.TranslationMiddleware'
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.contrib.messages.context_processors.messages',
	'beoi.core.changelang_context_proc',
	'beoi.core.contest_context'
)

ROOT_URLCONF = 'beoi.urls'

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates').replace('\\','/'),
)

INSTALLED_APPS = (
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.sites',
	'django.contrib.messages',
	'django.contrib.admin',
	'django.contrib.admindocs',
	'beoi.oi_core',
	'beoi.news',
	'beoi.contest',
)
