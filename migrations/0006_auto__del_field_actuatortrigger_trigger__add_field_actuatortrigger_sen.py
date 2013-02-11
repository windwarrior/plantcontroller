# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'ActuatorTrigger.trigger'
        db.delete_column('plantcontroller_actuatortrigger', 'trigger_id')

        # Adding field 'ActuatorTrigger.sensortype'
        db.add_column('plantcontroller_actuatortrigger', 'sensortype',
                      self.gf('django.db.models.fields.related.ForeignKey')(default='', to=orm['plantcontroller.SensorType']),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'ActuatorTrigger.trigger'
        db.add_column('plantcontroller_actuatortrigger', 'trigger',
                      self.gf('django.db.models.fields.related.ForeignKey')(default='', to=orm['plantcontroller.SensorType']),
                      keep_default=False)

        # Deleting field 'ActuatorTrigger.sensortype'
        db.delete_column('plantcontroller_actuatortrigger', 'sensortype_id')


    models = {
        'plantcontroller.actuatortrigger': {
            'Meta': {'object_name': 'ActuatorTrigger'},
            'below_value': ('django.db.models.fields.FloatField', [], {}),
            'date_end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_start': ('django.db.models.fields.DateTimeField', [], {}),
            'for_minutes': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sensortype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['plantcontroller.SensorType']"})
        },
        'plantcontroller.basereading': {
            'Meta': {'object_name': 'BaseReading'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value_in_reading': ('django.db.models.fields.FloatField', [], {}),
            'value_in_unit': ('django.db.models.fields.FloatField', [], {})
        },
        'plantcontroller.sensorreading': {
            'Meta': {'object_name': 'SensorReading'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reading': ('django.db.models.fields.FloatField', [], {}),
            'samples': ('django.db.models.fields.IntegerField', [], {}),
            'sensortype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['plantcontroller.SensorType']"}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        'plantcontroller.sensortype': {
            'Meta': {'object_name': 'SensorType'},
            'base_readings': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['plantcontroller.BaseReading']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'scale_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'unit_type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        }
    }

    complete_apps = ['plantcontroller']