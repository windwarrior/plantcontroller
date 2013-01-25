# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ActuatorTrigger'
        db.create_table('plantcontroller_actuatortrigger', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('below_value', self.gf('django.db.models.fields.FloatField')()),
            ('for_readings', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('plantcontroller', ['ActuatorTrigger'])

        # Adding model 'BaseReading'
        db.create_table('plantcontroller_basereading', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value_in_unit', self.gf('django.db.models.fields.FloatField')()),
            ('value_in_reading', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('plantcontroller', ['BaseReading'])

        # Adding model 'SensorType'
        db.create_table('plantcontroller_sensortype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=75)),
            ('unit_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('scale_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('trigger', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['plantcontroller.ActuatorTrigger'])),
        ))
        db.send_create_signal('plantcontroller', ['SensorType'])

        # Adding M2M table for field base_readings on 'SensorType'
        db.create_table('plantcontroller_sensortype_base_readings', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('sensortype', models.ForeignKey(orm['plantcontroller.sensortype'], null=False)),
            ('basereading', models.ForeignKey(orm['plantcontroller.basereading'], null=False))
        ))
        db.create_unique('plantcontroller_sensortype_base_readings', ['sensortype_id', 'basereading_id'])

        # Adding model 'SensorReading'
        db.create_table('plantcontroller_sensorreading', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('reading', self.gf('django.db.models.fields.FloatField')()),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('samples', self.gf('django.db.models.fields.IntegerField')()),
            ('sensortype', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['plantcontroller.SensorType'])),
        ))
        db.send_create_signal('plantcontroller', ['SensorReading'])


    def backwards(self, orm):
        # Deleting model 'ActuatorTrigger'
        db.delete_table('plantcontroller_actuatortrigger')

        # Deleting model 'BaseReading'
        db.delete_table('plantcontroller_basereading')

        # Deleting model 'SensorType'
        db.delete_table('plantcontroller_sensortype')

        # Removing M2M table for field base_readings on 'SensorType'
        db.delete_table('plantcontroller_sensortype_base_readings')

        # Deleting model 'SensorReading'
        db.delete_table('plantcontroller_sensorreading')


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
            'trigger': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['plantcontroller.ActuatorTrigger']"}),
            'unit_type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        }
    }

    complete_apps = ['plantcontroller']