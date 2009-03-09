"""
views for django-markitup

Time-stamp: <2009-03-09 13:42:35 carljm views.py>

"""
from markdown import markdown
from django.template.context import RequestContext
from django.shortcuts import render_to_response

def apply_markdown(request):
    markup = markdown(request.POST.get('data', ''))
    return render_to_response( 'markitup/preview.html',
                              {'preview':markup},
                              context_instance=RequestContext(request))
