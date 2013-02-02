#TODO: Maybe JSON-RPC is way too difficult for our arduino to talk with, maybe just use regular easy posts

from jsonrpc import jsonrpc_method
import random, pytz
from plantcontroller.models import SensorReading
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

        print this_dict
        result.append(this_dict)

    return result


