from django import template
from django.conf import settings
from markitup.settings import MARKITUP_SKIN, MARKITUP_SET, JQUERY_URL

register = template.Library()

_markitup_context = {
    'MARKITUP_SET': MARKITUP_SET,
    'MARKITUP_SKIN': MARKITUP_SKIN,
    'JQUERY_URL': JQUERY_URL,
    'MEDIA_URL': settings.MEDIA_URL}

@register.inclusion_tag('markitup/include_all.html')
def markitup_head(no_jquery=False):
    include_jquery = not bool(no_jquery)
    return dict(_markitup_context, include_jquery=include_jquery)

@register.inclusion_tag('markitup/include_js.html')
def markitup_js(no_jquery=False):
    include_jquery = not bool(no_jquery)
    return dict(_markitup_context, include_jquery=include_jquery)

@register.inclusion_tag('markitup/include_css.html')
def markitup_css():
    return _markitup_context

@register.inclusion_tag('markitup/editor.html')
def markitup_editor(textarea_id):
    return {'textarea_id': textarea_id}
