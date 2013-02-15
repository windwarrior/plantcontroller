from django.http import HttpResponse

def require_ip(ips):
    def decorator(func):
        def check_ip(request, *args, **kwargs):
            print "Checking IP"
            if(request.META['REMOTE_ADDR'] in ips):
                return func(request, *args, **kwargs)
            else:
                return HttpResponse("E:Acces Denied")
        return check_ip
    return decorator
