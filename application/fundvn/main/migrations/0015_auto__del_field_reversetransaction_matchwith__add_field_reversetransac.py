# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'ReverseTransaction.matchwith'
        db.delete_column('main_reversetransaction', 'matchwith')

        # Adding field 'ReverseTransaction.org_tran'
        db.add_column('main_reversetransaction', 'org_tran', self.gf('django.db.models.fields.related.ForeignKey')(related_name='reverse_tran', null=True, to=orm['main.Transaction']), keep_default=False)

        # Deleting field 'Transaction.matchwith'
        db.delete_column('main_transaction', 'matchwith')


    def backwards(self, orm):
        
        # User chose to not deal with backwards NULL issues for 'ReverseTransaction.matchwith'
        raise RuntimeError("Cannot reverse this migration. 'ReverseTransaction.matchwith' and its values cannot be restored.")

        # Deleting field 'ReverseTransaction.org_tran'
        db.delete_column('main_reversetransaction', 'org_tran_id')

        # User chose to not deal with backwards NULL issues for 'Transaction.matchwith'
        raise RuntimeError("Cannot reverse this migration. 'Transaction.matchwith' and its values cannot be restored.")


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
            'accountfirstname': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'accountlastname': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'accountnum': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'bank': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Bank']"}),
            'createdby': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'creator_of_sender_account'", 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'routingnum': ('django.db.models.fields.IntegerField', [], {})
        },
        'main.recipientbankaccount': {
            'Meta': {'object_name': 'RecipientBankAccount'},
            'accountfirstname': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'accountlastname': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'accountnum': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'bank': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Bank']"}),
            'createdby': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'creator_of_recipient_account'", 'null': 'True', 'to': "orm['auth.User']"}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'routingnum': ('django.db.models.fields.IntegerField', [], {})
        },
        'main.reversetransaction': {
            'Meta': {'object_name': 'ReverseTransaction'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'created': ('django.db.models.fields.DateField', [], {}),
            'createdby': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'org_tran': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reverse_tran'", 'null': 'True', 'to': "orm['main.Transaction']"}),
            'receiver': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reverse_transactions_received'", 'to': "orm['main.RecipientBankAccount']"}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reverse_transactions_sent'", 'to': "orm['main.MyBankAccount']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'N'", 'max_length': '1'})
        },
        'main.transaction': {
            'Meta': {'object_name': 'Transaction'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'created': ('django.db.models.fields.DateField', [], {}),
            'createdby': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'receiver': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transactions_received'", 'to': "orm['main.RecipientBankAccount']"}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transactions_sent'", 'to': "orm['main.MyBankAccount']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'N'", 'max_length': '1'})
        }
    }

    complete_apps = ['main']
