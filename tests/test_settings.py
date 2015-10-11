from __future__ import unicode_literals

from os.path import dirname

MIU_TEST_ROOT = dirname(__file__)

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

STATIC_URL = "/static/"

ROOT_URLCONF = "tests.urls"

# Use str so this isn't unicode on python 2
MARKITUP_FILTER = (str("tests.filter.testfilter"), {"arg": "replacement"})

SECRET_KEY = 'test-secret'

MIDDLEWARE_CLASSES = []
