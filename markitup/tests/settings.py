DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = 'markitup.db'

MARKUP_FILTER = ('markdown.markdown', {'safe_mode': True})

INSTALLED_APPS = (
    'markitup.tests',
)
