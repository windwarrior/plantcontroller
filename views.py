# Create your views here.
from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.views import login


def monitor(request):
    return render_to_response('sensor.html', RequestContext(request, {}))

def login_wrapper(request):
    return login(request, template_name='login_plantcontrol.html')


    
