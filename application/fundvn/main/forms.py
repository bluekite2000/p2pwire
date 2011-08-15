from django import forms
from django.forms import formsets
from django.db import models
from fundvn.main.models import *
from django.forms import fields
from django.forms.models import ModelForm, BaseModelFormSet,modelformset_factory 
from models import RecipientBankAccount
from models import MyBankAccount


class WaitList(forms.Form):
	My_name_is = forms.CharField(max_length=20)
	My_email_is = forms.CharField(max_length=20)

#TRANSACTION FORMS
class SearchForm(forms.Form):

	sender_country=forms.ModelChoiceField(queryset=Country.objects.all(), required=False)
	sender_city=forms.ModelChoiceField(queryset=City.objects.all(), required=False)
	receiver_country=forms.ModelChoiceField(queryset=Country.objects.all(), required=False)
	receiver_city=forms.ModelChoiceField(queryset=City.objects.all(), required=False)
	min_amount=forms.FloatField(required=False,label='with amount from')
	max_amount=forms.FloatField(required=False,label='to')
	def __init__(self, *args, **kwargs):
		#import pdb
		#pdb.set_trace()
		super(SearchForm, self).__init__(*args, **kwargs)
		
		self.fields['sender_city'].queryset=City.objects.filter(countryname=1) #countryname is vietnam
		self.fields['receiver_country'].queryset=Country.objects.filter(id=2)	#countryname is us
		self.fields['receiver_city'].queryset=City.objects.filter(countryname=2) #countryname is us

		modelchoicefields = [field for field_name, field in self.fields.iteritems() if isinstance(field, forms.ModelChoiceField)]
		for field in modelchoicefields:
			field.empty_label = None
class TransactionForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):

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
class MyBankAccountFormSet(BaseModelFormSet): 
  def __init__(self, *args, **kwargs): 
    #import pdb
    #pdb.set_trace()
    #self.queryset = kwargs.pop('queryset', [])
    self.user = kwargs.pop('user') 
    super(MyBankAccountFormSet, self).__init__(*args, **kwargs) 
    self.queryset = kwargs.pop('queryset', [])
  def _construct_form(self, i, **kwargs): 
    kwargs['user'] = self.user 
    """
    if self.queryset:
        #try:
            kwargs['queryset'] = self.queryset[i]
        except IndexError:
            pass
    """    
    return super(MyBankAccountFormSet, self)._construct_form(i, **kwargs) 



class MyBankAccountForm(ModelForm): 
  def __init__(self, *args, **kwargs): 
    #import pdb
    #pdb.set_trace()
    self.createdby = kwargs.pop('user') 
    super(MyBankAccountForm, self).__init__(*args, **kwargs) 

  class Meta:
   model = MyBankAccount
  def clean(self): 
    # use self.user 
    return self.cleaned_data 
   

  def save(self, commit=True):
      inst = super(MyBankAccountForm, self).save(commit=False)
      inst.createdby = self.createdby
      if commit:
          inst.save()
      return inst


MyBankAccountFormset = modelformset_factory(MyBankAccount, form=MyBankAccountForm, 
    formset=MyBankAccountFormSet, extra=1, max_num=1,exclude=('createdby')) 

		
#RECIPIENT BANK ACCOUNT FORM		
class RecipientBankAccountFormSet(BaseModelFormSet): 
  def __init__(self, *args, **kwargs): 
    #import pdb
    #pdb.set_trace()
    #self.queryset = kwargs.pop('queryset', [])
    self.user = kwargs.pop('user') 
    super(RecipientBankAccountFormSet, self).__init__(*args, **kwargs) 
    self.queryset = kwargs.pop('queryset', [])
  def _construct_form(self, i, **kwargs): 
    kwargs['user'] = self.user 
    """
    if self.queryset:
        #try:
            kwargs['queryset'] = self.queryset[i]
        except IndexError:
            pass
    """    
    return super(RecipientBankAccountFormSet, self)._construct_form(i, **kwargs) 



class RecipientBankAccountForm(ModelForm): 
  def __init__(self, *args, **kwargs): 
    #import pdb
    #pdb.set_trace()
    self.createdby = kwargs.pop('user') 
    super(RecipientBankAccountForm, self).__init__(*args, **kwargs) 

  class Meta:
   model = RecipientBankAccount
  def clean(self): 
    # use self.user 
    return self.cleaned_data 
   

  def save(self, commit=True):
      inst = super(RecipientBankAccountForm, self).save(commit=False)
      inst.createdby = self.createdby
      if commit:
          inst.save()
      return inst


RecipientBankAccountFormset = modelformset_factory(RecipientBankAccount, form=RecipientBankAccountForm, 
    formset=RecipientBankAccountFormSet, extra=1, max_num=1,exclude=('createdby')) 
