from django import template
from django.conf import settings as django_settings
from markitup import settings
from markitup.util import absolute_url

register = template.Library()

# we do some funny stuff here for testability (the tests need to be
# able to force a recalculation of this context)
def _get_markitup_context():
    return {
        'MARKITUP_SET': absolute_url(settings.MARKITUP_SET).rstrip('/'),
        'MARKITUP_SKIN': absolute_url(settings.MARKITUP_SKIN).rstrip('/'),
        'JQUERY_URL': absolute_url(settings.JQUERY_URL,
                                   django_settings.MEDIA_URL),
        'MARKITUP_JS': absolute_url('markitup/jquery.markitup.js')
        }
register._markitup_context = _get_markitup_context()

@register.inclusion_tag('markitup/include_all.html')
def markitup_media(no_jquery=False):
    include_jquery = not bool(no_jquery)
    return dict(register._markitup_context, include_jquery=include_jquery)

@register.inclusion_tag('markitup/include_js.html')
def markitup_js(no_jquery=False):
    include_jquery = not bool(no_jquery)
    return dict(register._markitup_context, include_jquery=include_jquery)

@register.inclusion_tag('markitup/include_css.html')
def markitup_css():
    return register._markitup_context

@register.inclusion_tag('markitup/editor.html')
def markitup_editor(textarea_id):
    return {'textarea_id': textarea_id}
