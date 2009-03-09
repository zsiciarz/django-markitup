from django.conf.urls.defaults import *

from markitup.views import apply_markdown

urlpatterns = patterns(
    '',
    url(r'markdown/$', apply_markdown, name='markitup_markdown')
    )
