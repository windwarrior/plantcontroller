from jsonrpc import jsonrpc_method
import random, pytz
from plantcontroller.models import SensorReading, SensorType, ActuatorTrigger
from plantcontroller.utils import *

from datetime import datetime, timedelta
from django.utils.timezone import utc
from django.utils import timezone

current_version = 1

@jsonrpc_method('getVersion() -> Number')
def get_version(request):
    return current_version

"""
The amount of hours * 60 divided by the amount of datapoints should yield an integer
"""
@jsonrpc_method('getDataPoints(Number, Number, Number) -> Array')
def get_data_points(request, interval, datapoints, offset):
    #Used to get datapoints for the webinterface, called by the clientside javascript
 
    #The resulting datapoints are averages from all points around that point
    half_interval_minutes = int(interval / 2)
    half_interval_seconds = int(((interval*1.0 / 2.0) - half_interval_minutes) * 60)

    #The total offset is the specified offset plus the interval times the amount of points
    total_offset = offset + interval * datapoints

    #(2013,1,22,4,0,0)
    end = floor_time(datetime.utcnow().replace(tzinfo=utc) - timedelta(minutes=(offset-half_interval_minutes), seconds=(-1 * half_interval_seconds)), interval)

    start = end - timedelta(minutes=total_offset+half_interval_minutes, seconds=half_interval_seconds)

    readings = SensorReading.objects.filter(datetime__gte=start, datetime__lte=end)


    result = []
    for i in range(0,datapoints):
        set_points = [x.reading for x in readings if x.datetime > (start + timedelta(minutes=interval*i)) and x.datetime <= (start + timedelta(minutes=interval*(i+1)))]
        this_point = sum(set_points) / len(set_points) if len(set_points) > 0 else 0

        datapoint_time = timezone.localtime(start + timedelta(minutes=interval*i+half_interval_minutes, seconds=half_interval_seconds))

        this_dict = {}
        this_dict["datapoint"] = this_point
        this_dict["time"] =  datapoint_time.strftime('%H:%M')

        result.append(this_dict)

    return result

@jsonrpc_method('getCurrentActuatorTrigger(String) -> Object')
def get_current_actuator_trigger(request, sensortype):
    print "ohai"
    sen_type = SensorType.objects.filter(name=sensortype)
    if len(sen_type) > 0:
        s = sen_type[0]
        r = ActuatorTrigger.objects.filter(sensortype = s, date_start__lte = datetime.utcnow().replace(tzinfo=utc)).exclude(date_end=None)
        return r[0].as_dict() if len(r) > 0 else {"error": "no triggers", "threshold": 0.00, "delay": 0}
    else:
        return {"error": "sensortype not found", "threshold": 0.00, "delay": 0}

@jsonrpc_method('storeActuatorTrigger(String, Number, Number) -> Boolean')
def store_actuator_trigger(request, sensortype, delay, threshold):
    try:
        sen_type = SensorType.objects.filter(name=sensortype)
        
        print "{0} {1}".format(threshold, (threshold/1023.0))

        if len(sen_type) > 0:
            new_trigger = ActuatorTrigger(below_value=(threshold/1023.0), sensortype=sen_type[0], date_start = datetime.utcnow().replace(tzinfo=utc), for_minutes=delay)

            old_triggers = ActuatorTrigger.objects.filter(date_end=None)

            for trig in old_triggers:
                trig.date_end = datetime.utcnow().replace(tzinfo=utc)
                trig.save()

            new_trigger.save()

            print "Saved {}".format(new_trigger.as_dict())

            return True

        return False
    except Exception as e:
        print str(e)



