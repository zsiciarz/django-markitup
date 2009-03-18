"""
views for django-markitup

Time-stamp: <2009-03-18 11:24:32 carljm views.py>

"""
from django.template.context import RequestContext
from django.shortcuts import render_to_response

from markitup.markup import filter_func

def apply_filter(request):
    markup = filter_func(request.POST.get('data', ''))
    return render_to_response( 'markitup/preview.html',
                              {'preview':markup},
                              context_instance=RequestContext(request))
