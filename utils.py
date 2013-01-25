from datetime import datetime

"""
Returns the datetime specified floored to the previous multiple of minutes
    floor_time(2013-01-21 12:18, 5) would result in 12:15
"""
def floor_time(dto, minutes):
    time_minute = dto.minute
    
    return dto.replace(minute=time_minute - (time_minute % minutes), second=0)


def ceiling_time(dto, minutes):
    time_minute = dto.minute

    return dto.replace(minute=(time_minute + minutes) - (time_minute % minutes), second=0)
