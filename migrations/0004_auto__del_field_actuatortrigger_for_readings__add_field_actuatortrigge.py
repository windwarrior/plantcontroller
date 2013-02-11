# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'ActuatorTrigger.for_readings'
        db.delete_column('plantcontroller_actuatortrigger', 'for_readings')

        # Adding field 'ActuatorTrigger.date_start'
        db.add_column('plantcontroller_actuatortrigger', 'date_start',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 2, 10, 0, 0)),
                      keep_default=False)

        # Adding field 'ActuatorTrigger.date_end'
        db.add_column('plantcontroller_actuatortrigger', 'date_end',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'ActuatorTrigger.for_minutes'
        db.add_column('plantcontroller_actuatortrigger', 'for_minutes',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'ActuatorTrigger.for_readings'
        db.add_column('plantcontroller_actuatortrigger', 'for_readings',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Deleting field 'ActuatorTrigger.date_start'
        db.delete_column('plantcontroller_actuatortrigger', 'date_start')

        # Deleting field 'ActuatorTrigger.date_end'
        db.delete_column('plantcontroller_actuatortrigger', 'date_end')

        # Deleting field 'ActuatorTrigger.for_minutes'
        db.delete_column('plantcontroller_actuatortrigger', 'for_minutes')


    models = {
        'plantcontroller.actuatortrigger': {
            'Meta': {'object_name': 'ActuatorTrigger'},
            'below_value': ('django.db.models.fields.FloatField', [], {}),
            'date_end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_start': ('django.db.models.fields.DateTimeField', [], {}),
            'for_minutes': ('django.db.models.fields.IntegerField', [], {}),
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
            'sensortype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['plantcontroller.SensorType']"}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '25'})
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