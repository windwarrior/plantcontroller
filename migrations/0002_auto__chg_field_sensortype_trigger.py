# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'SensorType.trigger'
        db.alter_column('plantcontroller_sensortype', 'trigger_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['plantcontroller.ActuatorTrigger'], null=True))

    def backwards(self, orm):

        # Changing field 'SensorType.trigger'
        db.alter_column('plantcontroller_sensortype', 'trigger_id', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['plantcontroller.ActuatorTrigger']))

    models = {
        'plantcontroller.actuatortrigger': {
            'Meta': {'object_name': 'ActuatorTrigger'},
            'below_value': ('django.db.models.fields.FloatField', [], {}),
            'for_readings': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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
            'sensortype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['plantcontroller.SensorType']"})
        },
        'plantcontroller.sensortype': {
            'Meta': {'object_name': 'SensorType'},
            'base_readings': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['plantcontroller.BaseReading']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'scale_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'trigger': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['plantcontroller.ActuatorTrigger']", 'null': 'True', 'blank': 'True'}),
            'unit_type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        }
    }

    complete_apps = ['plantcontroller']