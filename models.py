from django.db import models

# Create your models here.

UNITS = (
    ('c', 'celcius'),
    ('r', 'ohm'),
    ('l', 'lumen'),
    ('u', 'undefined'),
)

SCALES = (
    ('l', 'linear'),
    ('e', 'exponential'),
    ('u', 'undefined'),
)

"""
The type of sensor used, for example a thermometer
"""
class SensorType(models.Model):
    #Name of this sensortype
    name = models.CharField(max_length=75)

    #Unit eg. celcius, ohm, etc.
    unit_type = models.CharField(max_length=1, choices=UNITS)

    #Type of scale, exponential, linear... etc. designed to be easily expandable while keeping a fixed set of options
    scale_type = models.CharField(max_length=1, choices=SCALES)   

    def __unicode__(self):
        return unicode(self.name)

"""
Used to determin the scale.
For example lets say that we are measuring temperature
    a temperature of 0 degrees gives a 'reading' of 0.2
    a temperature of 100 degrees a 'reading' of 0.7
Then we can determin what a 'reading' of 0.4 would give, given that the growth is known (linear, exponential...)
"""

class BaseReading(models.Model):
    #eg. 20 (celcius)
    value_in_unit = models.FloatField()

    #eg. 0.789 (on a scale from 0.0 to 1.0)
    value_in_reading = models.FloatField()

    sensortype = models.ForeignKey(SensorType)
    
"""
A single datapoint taken from a sensor
"""
class SensorReading(models.Model):
    #Should be a reading between 0.0 and 1.0, probably the ADC reading divided by the ADC resolution
    reading = models.FloatField()

    #The date and time that this reading was made
    #Should be updated every minute, could differ slightly
    datetime = models.DateTimeField()

    #for future use, the amount of samples used to generate this reading
    samples = models.IntegerField()

    #what type of sensor is this, used to define scales and unit etc.
    sensortype = models.ForeignKey(SensorType)

    #source
    source = models.CharField(max_length=25)

    def __unicode__(self):
        date = self.datetime.strftime('%y-%m-%d %H:%M:%S')
        return "[{0}] Reading {1}".format(date, self.reading)

"""
An actuator trigger is the mechanism that the system uses to trigger a specific actuator
For example watering:
    when the relative value of the sensor is below 0.7 for 5 minutes

Then the ActuatorTrigger would be
    below_value = 0.7
    for_readings = 5 # one reading per minute
"""

class ActuatorTrigger(models.Model):
    #when to trigger
    date_start = models.DateTimeField()
    
    date_end = models.DateTimeField(blank = True, null = True)

    below_value = models.FloatField()

    for_minutes = models.IntegerField()

    #The trigger that measures whether to enable the actuator related to this sensor
    #TODO: when triggered, is a cooldown required?
    #TODO: what about toggleable systems like heaters
    sensortype = models.ForeignKey(SensorType)

    def as_dict(self):
        return {"threshold": self.below_value * 1023, "delay": self.for_minutes}
