from django.conf.urls import patterns, url, include
from django.views.generic.base import TemplateView

from .forms import DemoForm


urlpatterns = patterns(
    '',
    url(
        r'^$',
        TemplateView.as_view(template_name='demo.html'),
        {'form': DemoForm()},
        name='demo',
        ),
    url(r'^markitup/', include('markitup.urls')),
    )
