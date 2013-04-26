from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
    url(r'^markitup/', include('markitup.urls')),
    )
