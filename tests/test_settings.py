from __future__ import unicode_literals

from os.path import dirname, abspath, join

BASE_DIR = dirname(abspath(__file__))

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "markitup",
    "tests",
    "tests.test_migration",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3"
        }
    }

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

STATIC_URL = "/static/"

ROOT_URLCONF = "tests.urls"

# Use str so this isn't unicode on python 2
MARKITUP_FILTER = (str("tests.filter.testfilter"), {"arg": "replacement"})

SECRET_KEY = 'test-secret'

MIDDLEWARE_CLASSES = []
