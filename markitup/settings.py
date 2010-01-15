from django.conf import settings
import posixpath


MARKITUP_PREVIEW_FILTER = getattr(settings, 'MARKITUP_PREVIEW_FILTER',
                                  getattr(settings, 'MARKITUP_FILTER', None))
MARKITUP_AUTO_PREVIEW = getattr(settings, 'MARKITUP_AUTO_PREVIEW', False)
MARKITUP_MEDIA_URL = getattr(settings, 'MARKITUP_MEDIA_URL', settings.MEDIA_URL)
MARKITUP_SET = getattr(settings, 'MARKITUP_SET', 'markitup/sets/default')
MARKITUP_SKIN = getattr(settings, 'MARKITUP_SKIN', 'markitup/skins/simple')
JQUERY_URL = getattr(
    settings, 'JQUERY_URL',
    'http://ajax.googleapis.com/ajax/libs/jquery/1.4/jquery.min.js')
