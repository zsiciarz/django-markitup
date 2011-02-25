import posixpath
from django.conf import settings as django_settings
from markitup import settings

def absolute_url(path, prefix=None):
    if prefix is None:
        prefix = settings.MARKITUP_MEDIA_URL
    if path.startswith(u'http://') or path.startswith(u'https://') or path.startswith(u'/'):
        return path
    return posixpath.join(prefix, path)

def absolute_jquery_url():
    # JQuery absolute URL should be relative to STATIC_URL (or MEDIA_URL for
    # django < 1.3), not to MARKITUP_MEDIA_URL.
    return absolute_url(settings.JQUERY_URL,
                        getattr(django_settings, 'STATIC_URL',
                        django_settings.MEDIA_URL))
