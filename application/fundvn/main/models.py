from django.db import models
from django.contrib.auth.models import User
from smart_selects.db_fields import ChainedForeignKey 

class Country(models.Model):
	countryname=models.CharField(max_length=20)
	def __unicode__(self):
		return "%s"% (self.countryname)
class City(models.Model):
	cityname=models.CharField(max_length=20)
	countryname=models.ForeignKey(Country)
	def __unicode__(self):
		return " %s "% (self.cityname)	
		

class Bank(models.Model):
	bankname=models.CharField(max_length=20)
	banktype=models.CharField(max_length=20) #checking/saving/etc
	bankcity=models.ForeignKey(City)	
	bankcountry=models.ForeignKey(Country)	
	def __unicode__(self):
		return "%s %s %s"%(self.bankname, self.bankcity, self.bankcountry)
	
		
class MyBankAccount(models.Model):

	
	bank=models.ForeignKey(Bank)
	accountfirstname=models.CharField(max_length=20)
	accountlastname=models.CharField(max_length=20)
	#accountowner=models.ForeignKey(User)
	accountnum=models.IntegerField(unique=True)
	routingnum=models.IntegerField()	
	createdby=models.ForeignKey(User,null=True, related_name="creator_of_sender_account")
	def __unicode__(self):
		return u'%s %s %s %s' % (self.bank, self.accountfirstname, self.accountlastname, self.accountnum)
class RecipientBankAccount(models.Model):

	bank=models.ForeignKey(Bank)
	accountfirstname=models.CharField(max_length=20)
	accountlastname=models.CharField(max_length=20)
	accountnum=models.IntegerField(unique=True)
	routingnum=models.IntegerField()	
	email=models.EmailField(max_length=20)	

	createdby=models.ForeignKey(User,null=True, related_name="creator_of_recipient_account")
	def __unicode__(self):
		return  u'%s  %s %s %s' % (self.bank,self.accountfirstname, self.accountlastname, self.accountnum)
		
TRANSACTION_STATUS = (
    ('N','Pending'),
    ('Y','Completed'),
)
class Transaction(models.Model):
	sender = models.ForeignKey(MyBankAccount, unique=False, related_name="transactions_sent") 
	receiver = models.ForeignKey(RecipientBankAccount, unique=False, related_name="transactions_received")
	created = models.DateField('transfer request date')
	amount = models.FloatField()
	createdby=models.ForeignKey(User,null=True)
	status = models.CharField(max_length=1, choices=TRANSACTION_STATUS,default='N')
	def __unicode__(self):
		return  u'%s %s %s %s %s' % (self.sender, self.receiver,self.created, self.amount,self.createdby)
	def get_absolute_url(self):
		from django.core.urlresolvers import reverse
	
		return reverse('user_public_past_trans', kwargs={ 'createdby': self.createdby})
	def get_swap_absolute_url(self):
		from django.core.urlresolvers import reverse

		return reverse('reverse_transfer', kwargs={ 'id': self.id})

class ReverseTransaction(models.Model):
	sender = models.ForeignKey(MyBankAccount, unique=False, related_name="reverse_transactions_sent") 
	receiver = models.ForeignKey(RecipientBankAccount, unique=False, related_name="reverse_transactions_received")
	created = models.DateField('transfer request date')
	amount = models.FloatField()
	createdby=models.ForeignKey(User,null=True)
	status = models.CharField(max_length=1, choices=TRANSACTION_STATUS,default='N')
	org_tran=models.ForeignKey(Transaction, null=True)
	def __unicode__(self):
		return  u'%s %s %s %s %s' % (self.sender, self.receiver,self.created, self.amount,self.createdby)
	def get_absolute_url(self):
		from django.core.urlresolvers import reverse
	
		return reverse('user_public_past_trans', kwargs={ 'createdby': self.createdby})
	def get_swap_absolute_url(self):
		from django.core.urlresolvers import reverse

		return reverse('reverse_transfer', kwargs={ 'id': self.id})
