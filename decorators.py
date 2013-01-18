from django.http import HttpResponse

def require_ip(ip):
    def decorator(func):
        def check_ip(request, *args, **kwargs):
            print "Checking IP"
            if(request.META['REMOTE_ADDR'] == ip):
                return func(request, *args, **kwargs)
            else:
                return HttpResponse("Acces Denied")
        return check_ip
    return decorator
