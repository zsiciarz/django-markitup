from os.path import dirname, join, abspath

BASE_DIR = dirname(abspath(__file__))

INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'markitup',
    ]

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

ROOT_URLCONF = 'tests.project.urls'

MARKITUP_FILTER = ('markdown.markdown', {'safe_mode': True})
MARKITUP_SET = 'markitup/sets/markdown/'  # Default includes trailing slash so that others know it's a directory

DEBUG = True

STATICFILES_DIRS = [join(BASE_DIR, 'static')]
STATIC_URL = '/static/'

SECRET_KEY = 'secret'

ALLOWED_HOSTS = ['localhost']
