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
@jsonrpc_method('getDataPoints(String, Number, Number, Number) -> Object')
def get_data_points(request, sensortype, interval, datapoints, offset):
    #Used to get datapoints for the webinterface, called by the clientside javascript
 
    #The resulting datapoints are averages from all points around that point
    half_interval_minutes = int(interval / 2)
    half_interval_seconds = int(((interval*1.0 / 2.0) - half_interval_minutes) * 60)

    #The total offset is the specified offset plus the interval times the amount of points
    total_offset = offset + interval * datapoints

    end = floor_time(datetime.utcnow().replace(tzinfo=utc) - timedelta(minutes=(offset-half_interval_minutes), seconds=(-1 * half_interval_seconds)), interval)

    start = end - timedelta(minutes=total_offset+half_interval_minutes, seconds=half_interval_seconds)

    sen_type = SensorType.objects.filter(name=sensortype)

    if len(sen_type) > 0:
        readings = SensorReading.objects.filter(datetime__gte=start, datetime__lte=end, sensortype=sen_type[0])


        result = []
        for i in range(0,datapoints):
            # Filter the readings in a group belonging to this final point, for 5 minutes samples that would be 12:37:31 - 12:42:30 for the point 12:40
            set_points = [x.reading for x in readings if x.datetime > (start + timedelta(minutes=interval*i)) and x.datetime <= (start + timedelta(minutes=interval*(i+1)))]
            this_point = sum(set_points) / len(set_points) if len(set_points) > 0 else 0

            # Make that time localtime, so that the webinterface doesnt show the UTC time
            datapoint_time = timezone.localtime(start + timedelta(minutes=interval*i+half_interval_minutes, seconds=half_interval_seconds))

            this_dict = {}
            this_dict["datapoint"] = this_point
            this_dict["time"] =  datapoint_time.strftime('%H:%M')

            result.append(this_dict)


        return {"points": result, "adc_max": 1023}

    return {"points": [], "adc_max": 0}

@jsonrpc_method('getCurrentActuatorTrigger(String) -> Object')
def get_current_actuator_trigger(request, sensortype):
    # Get the sensortype object for the requested trigger
    sen_type = SensorType.objects.filter(name=sensortype)
    if len(sen_type) > 0:
        # If that sensortype object exists, check for actuatortriggers
        s = sen_type[0]
        r = ActuatorTrigger.objects.filter(sensortype = s, date_start__lte = datetime.utcnow().replace(tzinfo=utc), date_end=None)
        if len(r) > 0:
            # if such a trigger exists, return it as dict
            res = r[0].as_dict()
            res["adc_max"] = 1023
            return res
        else:
            return {"error": "no triggers", "threshold": 0.00, "delay": 0, "adc_max": 1023}
    else:
        return {"error": "sensortype not found", "threshold": 0.00, "delay": 0}

@jsonrpc_method('storeActuatorTrigger(String, Number, Number) -> Boolean', authenticated=True)
def store_actuator_trigger(request, sensortype, delay, threshold):
    try:
        # Get the sensortype object
        sen_type = SensorType.objects.filter(name=sensortype)
        
        if len(sen_type) > 0:
            # A new trigger is created according to the values specified
            new_trigger = ActuatorTrigger(below_value=(threshold), sensortype=sen_type[0], date_start = datetime.utcnow().replace(tzinfo=utc), for_minutes=delay)

            # All old triggers should be set to inactive
            old_triggers = ActuatorTrigger.objects.filter(date_end=None)

            for trig in old_triggers:
                trig.date_end = datetime.utcnow().replace(tzinfo=utc)
                trig.save()

            # Save the new trigger
            new_trigger.save()

            print "Saved {}".format(new_trigger.as_dict())

            return True

        return False
    except Exception as e:
        print str(e)
        return False



