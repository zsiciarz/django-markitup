from __future__ import unicode_literals

from os.path import dirname

MIU_TEST_ROOT = dirname(__file__)

INSTALLED_APPS = [
    "markitup",
    "tests"]

try:
    # Add test_migrations if Django supports native migrations
    from django.db import migrations
    INSTALLED_APPS.append('tests.test_migration')
except ImportError:
    pass

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
