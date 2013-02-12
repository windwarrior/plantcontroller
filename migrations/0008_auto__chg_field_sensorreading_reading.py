# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'SensorReading.reading'
        db.alter_column('plantcontroller_sensorreading', 'reading', self.gf('django.db.models.fields.IntegerField')())

    def backwards(self, orm):

        # Changing field 'SensorReading.reading'
        db.alter_column('plantcontroller_sensorreading', 'reading', self.gf('django.db.models.fields.FloatField')())

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
            'sensortype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['plantcontroller.SensorType']"}),
            'value_in_reading': ('django.db.models.fields.FloatField', [], {}),
            'value_in_unit': ('django.db.models.fields.FloatField', [], {})
        },
        'plantcontroller.sensorreading': {
            'Meta': {'object_name': 'SensorReading'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reading': ('django.db.models.fields.IntegerField', [], {}),
            'samples': ('django.db.models.fields.IntegerField', [], {}),
            'sensortype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['plantcontroller.SensorType']"}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        'plantcontroller.sensortype': {
            'Meta': {'object_name': 'SensorType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'scale_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'unit_type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        }
    }

    complete_apps = ['plantcontroller']