from django.shortcuts import render_to_response
from django.template import RequestContext

from markitup import settings
from markitup.markup import filter_func

def apply_filter(request):
    markup = filter_func(request.POST.get('data', ''))
    return render_to_response( 'markitup/preview.html',
                              {'preview': markup,
                               'MARKITUP_MEDIA_URL': settings.MARKITUP_MEDIA_URL},
                              context_instance=RequestContext(request))
