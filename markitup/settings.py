"""
settings for django-markitup

Time-stamp: <2009-11-11 12:28:49 carljm settings.py>

"""
from django.conf import settings
import posixpath


MARKITUP_PREVIEW_FILTER = getattr(settings, 'MARKITUP_PREVIEW_FILTER',
                                  getattr(settings, 'MARKITUP_FILTER', None))

# Automaticly enable the markitup preview
MARKITUP_PREVIEW_AUTO = getattr(settings, 'MARKITUP_PREVIEW_AUTO', False)

MARKITUP_MEDIA_URL = getattr(settings, 'MARKITUP_MEDIA_URL', settings.MEDIA_URL)
MARKITUP_SET = getattr(settings, 'MARKITUP_SET', 'markitup/sets/default')
MARKITUP_SKIN = getattr(settings, 'MARKITUP_SKIN', 'markitup/skins/simple')
JQUERY_URL = getattr(
    settings, 'JQUERY_URL',
    'http://ajax.googleapis.com/ajax/libs/jquery/1.3/jquery.min.js')
