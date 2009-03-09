"""
widgets for django-markitup

Time-stamp: <2009-03-09 13:23:33 carljm widgets.py>

"""
from django import forms
from django.utils.safestring import mark_safe

class MarkItUpWidget(forms.Textarea):
    """
    Widget for a MarkItUp editor textarea.

    Takes two additional optional keyword arguments:

    ``miu_set``
        URL path (absolute or relative to MEDIA_URL) to MarkItUp
        button set directory.  Default: ``markitup/sets/default``.

    ``miu_skin``
        URL path (absolute or relative to MEDIA_URL) to MarkItUp skin
        directory.  Default: ``markitup/skins/simple``.
        
    """
    def __init__(self, attrs=None,
                 miu_set='markitup/sets/default',
                 miu_skin='markitup/skins/simple'):
        self.miu_set = miu_set
        self.miu_skin = miu_skin
        super(MarkItUpWidget, self).__init__(attrs)

    def _media(self):
        return forms.Media(css={'screen': ('%s/style.css' % self.miu_skin,
                                           '%s/style.css' % self.miu_set)},
                           js=('http://ajax.googleapis.com/ajax/libs/jquery/1.2.6/jquery.min.js',
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
        
