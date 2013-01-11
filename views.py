# Create your views here.
from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response


def monitor(request):
    return render_to_response('monitor.html', RequestContext(request, {}))


    
