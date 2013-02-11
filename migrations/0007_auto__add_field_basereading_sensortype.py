# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing M2M table for field base_readings on 'SensorType'
        db.delete_table('plantcontroller_sensortype_base_readings')

        # Adding field 'BaseReading.sensortype'
        db.add_column('plantcontroller_basereading', 'sensortype',
                      self.gf('django.db.models.fields.related.ForeignKey')(default='', to=orm['plantcontroller.SensorType']),
                      keep_default=False)


    def backwards(self, orm):
        # Adding M2M table for field base_readings on 'SensorType'
        db.create_table('plantcontroller_sensortype_base_readings', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('sensortype', models.ForeignKey(orm['plantcontroller.sensortype'], null=False)),
            ('basereading', models.ForeignKey(orm['plantcontroller.basereading'], null=False))
        ))
        db.create_unique('plantcontroller_sensortype_base_readings', ['sensortype_id', 'basereading_id'])

        # Deleting field 'BaseReading.sensortype'
        db.delete_column('plantcontroller_basereading', 'sensortype_id')


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
            'reading': ('django.db.models.fields.FloatField', [], {}),
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