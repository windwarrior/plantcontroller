from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def add_data_point(request):
    print "Hallo"
    print request.raw_post_data
    if request.method == "POST":
        query_dict = request.POST
        print query_dict


    return HttpResponse("Hoi")
