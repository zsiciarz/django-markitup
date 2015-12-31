from os.path import dirname, join, abspath

BASE_DIR = dirname(abspath(__file__))

INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'markitup',
    ]

TEMPLATE_DIRS = [join(BASE_DIR, 'templates')]

ROOT_URLCONF = 'tests.project.urls'

MARKITUP_FILTER = ('markdown.markdown', {'safe_mode': True})
MARKITUP_SET = 'markitup/sets/markdown/'  # Default includes trailing slash so that others know it's a directory

DEBUG = True

STATICFILES_DIRS = [join(BASE_DIR, 'static')]
STATIC_URL = '/static/'

SECRET_KEY = 'secret'

ALLOWED_HOSTS = ['localhost']
