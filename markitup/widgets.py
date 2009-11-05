"""
widgets for django-markitup

Time-stamp: <2009-03-18 11:50:47 carljm widgets.py>

"""
from django import forms
from django.utils.safestring import mark_safe
from django.contrib.admin.widgets import AdminTextareaWidget

from markitup.settings import MARKITUP_SET, MARKITUP_SKIN, JQUERY_URL

class MarkupTextarea(forms.Textarea):
    def render(self, name, value, attrs=None):
        if value is not None:
            # Special handling for MarkupField value.
            # This won't touch simple TextFields because they don't have
            # 'raw' attribute.
            try:
                value = value.raw
            except AttributeError:
                pass
        return super(MarkupTextarea, self).render(name, value, attrs)


class MarkItUpWidget(MarkupTextarea):
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

        self.miu_set = markitup_set or MARKITUP_SET
        self.miu_skin = markitup_skin or MARKITUP_SKIN
        super(MarkItUpWidget, self).__init__(attrs)

    def _media(self):
        return forms.Media(css={'screen': ('%s/style.css' % self.miu_skin,
                                           '%s/style.css' % self.miu_set)},
                           js=(JQUERY_URL,
                               'markitup/jquery.markitup.js',
                               '%s/set.js' % self.miu_set))
    media = property(_media)

    def render(self, name, value, attrs=None):
        html = super(MarkItUpWidget, self).render(name, value, attrs)
        html += ('<script type="text/javascript">'
                 '$(document).ready(function() {'
                 '  $("#%s").markItUp(mySettings);'
                 '});'
                 '</script>' % attrs['id'])
        return mark_safe(html)


class AdminMarkItUpWidget(MarkItUpWidget, AdminTextareaWidget):
    ''' It adds vLargeTextField class to textarea so it'll
        be more like standard admin Textarea.
    '''
    pass
