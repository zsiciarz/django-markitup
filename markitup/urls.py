from __future__ import unicode_literals

from django.conf.urls import patterns, url

from markitup.views import apply_filter

urlpatterns = patterns(
    '',
    url(r'preview/$', apply_filter, name='markitup_preview')
    )
