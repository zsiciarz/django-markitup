from os.path import dirname, join
MIU_TEST_ROOT = dirname(__file__)

SITE_ID = 1 # @@@ workaround bug in trunk create_test_db

INSTALLED_APPS = [
    "django.contrib.sites", # @@@ workaround bug in trunk create_test_db
    "markitup",
    "tests"]

from django import VERSION

if VERSION < (1, 2):
    DATABASE_ENGINE = "sqlite3"
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3"
            }
        }

MEDIA_URL = "/media/"
MEDIA_ROOT = join(dirname(MIU_TEST_ROOT), "markitup", "media")

STATIC_URL = "/static/"
STATIC_ROOT = MEDIA_ROOT

ROOT_URLCONF = "tests.urls"

MARKITUP_FILTER = ("tests.filter.testfilter", {"arg": "replacement"})
