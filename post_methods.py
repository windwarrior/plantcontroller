from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from plantcontroller.decorators import require_ip
from plantcontroller.models import SensorType, SensorReading, ActuatorTrigger
from datetime import datetime
from django.utils.timezone import utc

@csrf_exempt
@require_ip(['130.89.190.206', '86.90.155.93', '130.89.165.27', '130.89.162.163'])
def add_data_point(request):
    if request.method == "POST":
        try:
            # this is the dictionairy with the postdata of this request
            query_dict = request.POST
            print(query_dict)
            reading = int(query_dict.get('reading', '-1'))
            sensortype = query_dict.get('sensortype', 'none')
            samples = int(query_dict.get('samples', '-1'))
            source = query_dict.get('source', '')
            if reading >= 0 and samples >= 0:
                # Get the corresponding sensortype object, for example the object associated with "humidity"
                sensortypes = SensorType.objects.filter(name = sensortype)
                if len(sensortypes) == 0:
                    # If no sensortype object is found, this sensor is new, and has to be stored
                    sensortypes = [SensorType(name=sensortype,unit_type='u', scale_type='u', trigger=None)]
                    sensortypes[0].save()

                # Save the newly found reading
                reading = SensorReading(reading=reading, datetime=datetime.utcnow().replace(tzinfo=utc), samples=samples, sensortype=sensortypes[0], source=source)
                reading.save()

                # Check whether there is a trigger set for this sensortype
                triggers = ActuatorTrigger.objects.filter(date_end=None)

                if len(triggers) > 0:
                    current = triggers[0]

                    # Get all sensorreadings for this sensortype, order them by date
                    sr = SensorReading.objects.filter(sensortype=sensortypes[0]).order_by('-datetime')

                    # Get the oldest reading for which all sensorvalues after it are below threshold
                    threshold_time = getLatestBelowThreshold(sr, current.below_value)

                    if not threshold_time == None:
                        # The time between now and the latest datapoint below threshold
                        seconds_since_below_threshold = (datetime.utcnow().replace(tzinfo=utc) - threshold_time).total_seconds()

                        # The time that the sensor should be below threshold before taking action
                        seconds_in_trigger = current.for_minutes * 60

                        print "Below Treshold {0}, In trigger {1}".format(seconds_since_below_threshold, seconds_in_trigger)

                        if seconds_since_below_threshold - seconds_in_trigger > 0:
                            #TODO: hier weten we dus dat er water gegeven gaat worden! Misschien leuk voor in de webinterface?

                            return HttpResponse("W:0")
                        else:
                            #TODO: hier weten we dus dat er water gegeven kan zijn! Misschien leuk voor in de webinterface?

                            return HttpResponse("W:{0}<{1}".format(int(seconds_in_trigger - seconds_since_below_threshold), int(current.below_value)))

                    else:
                        return HttpResponse("E:No sensorreadings found :O?")    
                else:
                    return HttpResponse("E:No triggers")

                    
            else:
                return HttpResponse("E:Some values not defined")
                                
        except Exception as e:
            import traceback
            traceback.print_exc()
            return HttpResponse("E:{0}".format(e))


    return HttpResponse("E:This method is post only")

def getLatestBelowThreshold(iterable, threshold):
    prev = iterable[0] if len(iterable) > 0 else None

    #TODO: actually the correct time would be between the last reading that was above threshold and the first one that is above

    #Get the latest element of the list for which the reading is below threshold 
    for i in iterable:
        if i.reading >= threshold:
            break
        else:
            prev = i

    print "Threshold: {0}, higher reading {1}".format(threshold,prev.reading)

    # return the date for that reading, if such a reading exists
    return prev.datetime if prev else None
        
        
