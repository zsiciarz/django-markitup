from os.path import dirname, join
MIU_TEST_ROOT = dirname(__file__)

INSTALLED_APPS = ('markitup', 'tests')
DATABASE_ENGINE = 'sqlite3'

MEDIA_URL = '/media/'
MEDIA_ROOT = join(dirname(MIU_TEST_ROOT), 'markitup', 'media')

STATIC_URL = '/static/'
STATIC_ROOT = MEDIA_ROOT

ROOT_URLCONF = 'tests.urls'

MARKUP_FILTER = ('tests.filter.testfilter', {'arg': 'replacement'})
