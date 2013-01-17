#TODO: Maybe JSON-RPC is way too difficult for our arduino to talk with, maybe just use regular easy posts

from jsonrpc import jsonrpc_method
import random

current_version = 1

@jsonrpc_method('getVersion() -> Number')
def get_version(request):
    return current_version

def add_data_point(request, sensortype, value):
    #TODO: This method should also check whether the trigger that might be set should go off
    pass


@jsonrpc_method('getDataPoints(Number, Number) -> Array')
def get_data_points(request, hours, datapoints):
    #Used to get datapoints for the webinterface, called by the clientside javascript
    return [random.random() for i in range(0,datapoints)]


