# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'BankAccount'
        db.delete_table('main_bankaccount')

        # Adding model 'MyBankAccount'
        db.create_table('main_mybankaccount', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bank', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Bank'])),
            ('accountowner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('accountnum', self.gf('django.db.models.fields.FloatField')(unique=True)),
            ('routingnum', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('main', ['MyBankAccount'])

        # Adding model 'RecipientBankAccount'
        db.create_table('main_recipientbankaccount', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bank', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Bank'])),
            ('accountowner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('accountnum', self.gf('django.db.models.fields.FloatField')(unique=True)),
            ('routingnum', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('main', ['RecipientBankAccount'])

        # Changing field 'Transaction.sender'
        db.alter_column('main_transaction', 'sender_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.MyBankAccount']))

        # Changing field 'Transaction.receiver'
        db.alter_column('main_transaction', 'receiver_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.RecipientBankAccount']))

        db.rename_table('main_bankaccount', 'main_mybankaccount')


    def backwards(self, orm):
        
        # Adding model 'BankAccount'
        db.create_table('main_bankaccount', (
            ('accountnum', self.gf('django.db.models.fields.FloatField')(unique=True)),
            ('routingnum', self.gf('django.db.models.fields.FloatField')()),
            ('accountowner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bank', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Bank'])),
        ))
        db.send_create_signal('main', ['BankAccount'])

        # Deleting model 'MyBankAccount'
        db.delete_table('main_mybankaccount')

        # Deleting model 'RecipientBankAccount'
        db.delete_table('main_recipientbankaccount')

        # Changing field 'Transaction.sender'
        db.alter_column('main_transaction', 'sender_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.BankAccount']))

        # Changing field 'Transaction.receiver'
        db.alter_column('main_transaction', 'receiver_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.BankAccount']))
        db.rename_table('main_mybankaccount', 'main_bankaccount')


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
        'main.country': {
            'Meta': {'object_name': 'Country'},
            'countryname': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'main.mybankaccount': {
            'Meta': {'object_name': 'MyBankAccount'},
            'accountnum': ('django.db.models.fields.FloatField', [], {'unique': 'True'}),
            'accountowner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'bank': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Bank']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'routingnum': ('django.db.models.fields.FloatField', [], {})
        },
        'main.recipientbankaccount': {
            'Meta': {'object_name': 'RecipientBankAccount'},
            'accountnum': ('django.db.models.fields.FloatField', [], {'unique': 'True'}),
            'accountowner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'bank': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Bank']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'routingnum': ('django.db.models.fields.FloatField', [], {})
        },
        'main.transaction': {
            'Meta': {'object_name': 'Transaction'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'receiver': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transactions_received'", 'to': "orm['main.RecipientBankAccount']"}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transactions_sent'", 'to': "orm['main.MyBankAccount']"})
        }
    }

    complete_apps = ['main']
