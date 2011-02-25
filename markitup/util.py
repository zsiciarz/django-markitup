from markitup import settings
import posixpath

def absolute_url(path, prefix=None):
    if prefix is None:
        prefix = settings.MARKITUP_MEDIA_URL
    if path.startswith(u'http://') or path.startswith(u'https://') or path.startswith(u'/'):
        return path
    return posixpath.join(prefix, path)
