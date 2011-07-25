from django import forms
from django.db import models
#from django.forms.models import modelformset_factory
from fundvn.main.models import *


class WaitList(forms.Form):
	My_name_is = forms.CharField(max_length=20)
	My_email_is = forms.CharField(max_length=20)

#TRANSACTION FORMS
class SearchForm(forms.Form):
	sender_country=forms.CharField(max_length=20, required=False,label='Sender country')
	receiver_country=forms.CharField(max_length=20, required=False,label='Receiver country')
	min_amount=forms.FloatField(required=False,label='with amount from')
	max_amount=forms.FloatField(required=False,label='to')
	
class TransactionForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		#import pdb
		#pdb.set_trace()
		sender = kwargs.pop('sender',None)
		createdby=kwargs.pop('createdby',None)
		
		super(TransactionForm, self).__init__(*args, **kwargs)

		if sender:
			self.fields['sender'].queryset = MyBankAccount.objects.filter(createdby=createdby)
		if createdby:
			self.fields['receiver'].queryset=RecipientBankAccount.objects.filter(createdby=createdby)
		
		modelchoicefields = [field for field_name, field in self.fields.iteritems() if isinstance(field, forms.ModelChoiceField)]
		for field in modelchoicefields:
			field.empty_label = None
	class Meta:
		model = Transaction
		exclude = ('createdby',)
		fields = ['sender','receiver','created','amount',]
	def save(self, *args, **kwargs):
		u = self.instance
		u.save()
		transaction = super(TransactionForm, self).save(*args,**kwargs)
		return transaction
		
#this form is for sender who found a match. It is similar to transaction form,except it doesnt hide the status attribute
		
class PostTransactionForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		#import pdb
		#pdb.set_trace()
		sender = kwargs.pop('sender',None)
		createdby=kwargs.pop('createdby',None)
		
		super(PostTransactionForm, self).__init__(*args, **kwargs)

		if sender:
			self.fields['sender'].queryset = MyBankAccount.objects.filter(createdby=createdby)
		if createdby:
			self.fields['receiver'].queryset=RecipientBankAccount.objects.filter(createdby=createdby)
		
		modelchoicefields = [field for field_name, field in self.fields.iteritems() if isinstance(field, forms.ModelChoiceField)]
		for field in modelchoicefields:
			field.empty_label = None
	class Meta:
		model = Transaction
		exclude = ('createdby',)
		fields = ['sender','receiver','created','amount','status']
	def save(self, *args, **kwargs):
		u = self.instance
		u.save()
		transaction = super(PostTransactionForm, self).save(*args,**kwargs)
		return transaction	
		
#this form is similar to transaction form, except it is used by sender who wants to swap
		
class ReverseTransactionForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):

		sender = kwargs.pop('sender',None)
		createdby=kwargs.pop('createdby',None)
		
		super(ReverseTransactionForm, self).__init__(*args, **kwargs)

		if sender:
			self.fields['sender'].queryset = MyBankAccount.objects.filter(createdby=createdby)
		if createdby:
			self.fields['receiver'].queryset=RecipientBankAccount.objects.filter(createdby=createdby)
		
		modelchoicefields = [field for field_name, field in self.fields.iteritems() if isinstance(field, forms.ModelChoiceField)]
		for field in modelchoicefields:
			field.empty_label = None
			
	class Meta:
		model = ReverseTransaction
		exclude = ('createdby',)
	
		fields = ['sender','receiver','created','amount','createdby']
	def save(self, *args, **kwargs):
		u = self.instance
		u.save()
		transaction = super(ReverseTransactionForm, self).save(*args,**kwargs)
		return transaction

#BANK ACCOUNT FORM
class BankAccountForm(forms.ModelForm):
	
	def __init__(self, *args, **kwargs):
		super(BankAccountForm, self).__init__(*args, **kwargs)
		
	class Meta:
		model = MyBankAccount
		exclude = ('createdby',)
	def save(self, *args, **kwargs):
		u = self.instance
		u.save()
		mybankaccount = super(BankAccountForm, self).save(*args,**kwargs)
		return mybankaccount
		
		
#RECIPIENT BANK ACCOUNT FORM		
class RecipientBankAccountForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super(RecipientBankAccountForm, self).__init__(*args, **kwargs)

	class Meta:
		model = RecipientBankAccount
		exclude = ('createdby',)
	def save(self, *args, **kwargs):
		u = self.instance
		u.save()
		recipientbankaccount = super(RecipientBankAccountForm, self).save(*args,**kwargs)
		return recipientbankaccount