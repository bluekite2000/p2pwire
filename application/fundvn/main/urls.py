from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import direct_to_template
from django.views.generic import ListView, DetailView
from main.views import *
from models import Transaction
from models import MyBankAccount
from models import RecipientBankAccount

from profiles.forms import ProfileForm
from profiles.views import *


urlpatterns = patterns('main.views',
	#WAITING LIST
    url(r'^$', 'contact_form', name="contact_form"),
    url(r'^thanks/$', direct_to_template, {'template': 'thanks.html'},name="thanks"),
	url(r'^about/$',about,name='about'),
	url(r'^press/$',press,name='press'),
	url(r'^blog/$',blog,name='blog'),
	
	url(r'^main/$',main_home,name='main_home'),
    url(r'^(?P<username>\w+)/alltrans/$', searchpage, name="searchpage"),
	url(r'^citysearch/$', ajax_city_search, name ="city_search"),
	url(r'^public_trans/(?P<createdby>\w+)/$',user_public_past_trans,name="user_public_past_trans"),
	
	#TRANSACTION CREATE,EDIT AND ACCEPT
	url(r'^transfer/$',transfer,name='transfer'),
	url(r'^(?P<username>\w+)/trans/create/$', TransactionCreateView.as_view(model=Transaction)),
	url(r'^(?P<username>\w+)/trans/create/success/$',transaction_created,name='transaction_created'),
    url(r'^trans/edit/(\d+)/$', trans_edit, name="trans_edit"),
	url(r'^(?P<username>\w+)/trans/edit/(?P<pk>\d+)/$', PostTransactionUpdateView.as_view(model=Transaction)),
	url(r'^(?P<username>\w+)/trans/edit/(\d+)/success/$',trans_edited,name='trans_edited'),
 	url(r'^trans/accept/(\d+)/$', rtrans_accept, name="rtrans_accept"),
	url(r'^(?P<username>\w+)/trans/accept/(?P<id>\w+)/$', reverse_trans_accept, name="reverse_trans_accept"),
	
	#REVERSE TRANSACTION		
	url(r'^reverse_transfer/(?P<id>\w+)/$',reverse_transfer,name="reverse_transfer"),
	url(r'^(?P<username>\w+)/reverse_trans/(?P<id>\w+)/create/$', ReverseTransactionCreateView.as_view(model=ReverseTransaction,context_object_name="trans")),
	url(r'^(?P<username>\w+)/reverse_trans/(?P<id>\w+)/create/success/$',reverse_transaction_created,name='reverse_transaction_created'),
	
	#TRANSACT-list past transactions/reverse transactions-this page is shown in profile section
	url(r'^trans_history/$',trans_history,name='trans_history'),
	url(r'^reverse_trans_history/$',reverse_trans_history,name='reverse_trans_history'),
	url(r'^(?P<username>\w+)/trans/$',user_private_past_trans,name="user_private_past_trans"),
    url(r'^(?P<username>\w+)/reverse_trans/$',user_private_past_reverse_trans,name="user_private_past_reverse_trans"),
	
	#PROFILE-profile	
	url(r'^profile_home/$',profile_home,name='profile_home'),
	url(r'^(?P<username>\w+)/profiles/detail/$',profile_detail,name='profile_detail'),
	url(r'^profile_edit/$',profile_edit,name='profile_edit'),	                       
	url(r'^(?P<username>\w+)/profiles/edit/$',edit_profile,{'form_class': ProfileForm,'success_url':None,}),
	#PROFILE-bank-list all existing bank accounts
	url(r'^mybank_manage/$',mybank_manage,name='mybank_manage'),
	url(r'^(?P<username>\w+)/mybank/manage/$',ListView.as_view(model=MyBankAccount)),
	#PROFILE-bank-add a new bank account
	url(r'^mybank_add/$',mybank_add,name='mybank_add'),
	url(r'^(?P<username>\w+)/mybank/add/$',BankAccountCreateView.as_view(model=MyBankAccount)),
	url(r'^(?P<username>\w+)/mybank/add/success/$',mybank_added,name='mybank_added'),							
		
	#PROFILE-bank-edit an existing bank account		
    url(r'^mybank/edit/(\d+)/$', mybank_edit, name="mybank_edit"),
	url(r'^(?P<username>\w+)/mybank/edit/(?P<pk>\d+)/$', BankAccountUpdateView.as_view(model=MyBankAccount)),
	url(r'^(?P<username>\w+)/mybank/edit/(\d+)/success/$',mybank_edited,name='mybank_edited'),							
	#PROFILE-bank-delete an existing bank account
	url(r'^mybank/delete/(\d+)/$', mybank_delete, name="mybank_delete"),
	url(r'^(?P<username>\w+)/mybank/delete/(?P<pk>\d+)/$', BankAccountDeleteView.as_view(model=MyBankAccount)),
	url(r'^(?P<username>\w+)/mybank/delete/(\d+)/success/$',mybank_deleted,name='mybank_deleted'),
	
	#RECIPIENT-list all recipients		
	url(r'^recipient_manage/$',recipient_manage,name='recipient_manage'),
	url(r'^(?P<username>\w+)/recipient/manage/$',ListView.as_view(model=RecipientBankAccount)),												
	#RECIPIENT-add new recipient
	url(r'^recipient_add/$',recipient_add,name='recipient_add'),
	url(r'^(?P<username>\w+)/recipient/add/$',RecipientBankAccountCreateView.as_view(model=RecipientBankAccount)),
	url(r'^(?P<username>\w+)/recipient/add/success/$',recipient_added,name='recipient_added'),
	#RECIPIENT-edit existing recipient
	url(r'^recipientbank/edit/(\d+)/$',recipientbank_edit, name="recipientbank_edit"),
	url(r'^(?P<username>\w+)/recipientbank/edit/(?P<pk>\d+)/$', RecipientBankAccountUpdateView.as_view(model=RecipientBankAccount)),
	url(r'^(?P<username>\w+)/recipientbank/edit/(\d+)/success/$',recipientbank_edited,name='recipientbank_edited'),							
	#RECIPIENT-delete existing recipient
	url(r'^recipientbank/delete/(\d+)/$', recipientbank_delete, name="recipientbank_delete"),
	url(r'^(?P<username>\w+)/recipientbank/delete/(?P<pk>\d+)/$', RecipientBankAccountDeleteView.as_view(model=RecipientBankAccount)),
	url(r'^(?P<username>\w+)/recipientbank/delete/(\d+)/success/$',recipientbank_deleted,name='recipientbank_deleted'),
	




)
