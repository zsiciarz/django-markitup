from django.conf.urls import url, include
from django.views.generic.base import TemplateView

from .forms import DemoForm


urlpatterns = [
    url(
        r'^$',
        TemplateView.as_view(template_name='demo.html'),
        {'form': DemoForm()},
        name='demo',
        ),
    url(r'^markitup/', include('markitup.urls')),
]
