"""
widgets for django-markitup

Time-stamp: <2009-11-06 00:23:41 carljm widgets.py>

"""
from django import forms
from django.utils.safestring import mark_safe

from markitup import settings
from markitup.util import absolute_url
import posixpath

class MarkItUpWidget(forms.Textarea):
    """
    Widget for a MarkItUp editor textarea.

    Takes two additional optional keyword arguments:

    ``markitup_set``
        URL path (absolute or relative to MEDIA_URL) to MarkItUp
        button set directory.  Default: value of MARKITUP_SET setting.

    ``markitup_skin``
        URL path (absolute or relative to MEDIA_URL) to MarkItUp skin
        directory.  Default: value of MARKITUP_SKIN setting.
        
    """
    def __init__(self, attrs=None,
                 markitup_set=None,
                 markitup_skin=None):
        self.miu_set = absolute_url(markitup_set or settings.MARKITUP_SET)
        self.miu_skin = absolute_url(markitup_skin or settings.MARKITUP_SKIN)
        super(MarkItUpWidget, self).__init__(attrs)

    def _media(self):
        return forms.Media(
            css= {'screen': (posixpath.join(self.miu_skin, 'style.css'),
                             posixpath.join(self.miu_set, 'style.css'))},
            js=(settings.JQUERY_URL,
                absolute_url('markitup/jquery.markitup.js'),
                posixpath.join(self.miu_set, 'set.js')))
    media = property(_media)
        
    def render(self, name, value, attrs=None):
        html = super(MarkItUpWidget, self).render(name, value, attrs)
        html += ('<script type="text/javascript">'
                 '$(document).ready(function() {'
                 '  $("#%s").markItUp(mySettings);'
                 '});'
                 '</script>' % attrs['id'])
        return mark_safe(html)
        
