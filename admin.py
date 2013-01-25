from django.contrib import admin
from plantcontroller.models import ActuatorTrigger, BaseReading, SensorType, SensorReading

admin.site.register(ActuatorTrigger)
admin.site.register(BaseReading)
admin.site.register(SensorType)
admin.site.register(SensorReading)
