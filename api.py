#TODO: Maybe JSON-RPC is way too difficult for our arduino to talk with, maybe just use regular easy posts

from jsonrpc import jsonrpc_method

current_version = 1

@jsonrpc_method('getVersion() -> Number')
def get_version(request):
    return current_version


#@jsonrpc_method('addDataPoint(Char, Number) -> Boolean')
def add_data_point(request, sensortype, value):
    #TODO: This method should also check whether the trigger that might be set should go off
    pass


@jsonrpc_method('getDataPoints(String, String) -> Array')
def get_data_points(request, start_date, end_date):
    #Used to get datapoints for the webinterface, called by the clientside javascript
    pass

