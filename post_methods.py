from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from plantcontroller.decorators import require_ip
from plantcontroller.models import SensorType, SensorReading
from datetime import datetime
from django.utils.timezone import utc

@csrf_exempt
@require_ip(['130.89.190.206', '130.89.233.21', '86.90.155.93', '130.89.162.163'])
def add_data_point(request):
    print "Hallo"
    print request.raw_post_data
    if request.method == "POST":
        try:
            query_dict = request.POST
            reading = int(query_dict.get('reading', '-1'))
            sensortype = query_dict.get('sensortype', 'none')
            samples = int(query_dict.get('samples', '-1'))
            source = query_dict.get('source', '')
            if reading >= 0 and samples >= 0:
                sensortypes = SensorType.objects.filter(name = sensortype)
                if len(sensortypes) == 0:
                    sensortypes = [SensorType(name=sensortype,unit_type='u', scale_type='u', trigger=None)]
                    sensortypes[0].save()

                print datetime.utcnow().replace(tzinfo=utc)
                reading = SensorReading(reading=(reading/1023.0), datetime=datetime.utcnow().replace(tzinfo=utc), samples=samples, sensortype=sensortypes[0], source=source)
                reading.save()
            else:
                return HttpResponse("Some values not defined")
                                
        except Exception as e:
            print e
            return HttpResponse(e.strerror)


    return HttpResponse("Succes")
