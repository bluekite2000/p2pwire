# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Country'
        db.create_table('main_country', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('countryname', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('main', ['Country'])

        # Adding model 'Bank'
        db.create_table('main_bank', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bankname', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('banktype', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('bankcountry', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Country'])),
        ))
        db.send_create_signal('main', ['Bank'])

        # Adding model 'BankAccount'
        db.create_table('main_bankaccount', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bank', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Bank'])),
            ('accountowner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('accountnum', self.gf('django.db.models.fields.FloatField')()),
            ('routingnum', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('main', ['BankAccount'])

        # Adding model 'Transaction'
        db.create_table('main_transaction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sender', self.gf('django.db.models.fields.related.ForeignKey')(related_name='transactions_sent', unique=True, to=orm['main.BankAccount'])),
            ('receiver', self.gf('django.db.models.fields.related.ForeignKey')(related_name='transactions_received', unique=True, to=orm['main.BankAccount'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('main', ['Transaction'])


    def backwards(self, orm):
        
        # Deleting model 'Country'
        db.delete_table('main_country')

        # Deleting model 'Bank'
        db.delete_table('main_bank')

        # Deleting model 'BankAccount'
        db.delete_table('main_bankaccount')

        # Deleting model 'Transaction'
        db.delete_table('main_transaction')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'main.bank': {
            'Meta': {'object_name': 'Bank'},
            'bankcountry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Country']"}),
            'bankname': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'banktype': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'main.bankaccount': {
            'Meta': {'object_name': 'BankAccount'},
            'accountnum': ('django.db.models.fields.FloatField', [], {}),
            'accountowner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'bank': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Bank']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'routingnum': ('django.db.models.fields.FloatField', [], {})
        },
        'main.country': {
            'Meta': {'object_name': 'Country'},
            'countryname': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'main.transaction': {
            'Meta': {'object_name': 'Transaction'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'receiver': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transactions_received'", 'unique': 'True', 'to': "orm['main.BankAccount']"}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transactions_sent'", 'unique': 'True', 'to': "orm['main.BankAccount']"})
        }
    }

    complete_apps = ['main']
