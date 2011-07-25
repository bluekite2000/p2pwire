from django.http import HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import redirect, render
from django.core.mail import mail_admins
from forms import WaitList
from django.conf import settings
import os

from django.shortcuts import get_object_or_404
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from main.forms import *
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response
from main.models import *
from django.views.generic.list_detail import object_list

#static pages
def about(request):
    return render(request, 'main/about.html')
def press(request):
	return render(request, 'main/press.html')
def blog(request):
	return render(request, 'main/blog.html')
def contact_form(request):
    fileObj = open(settings.MEDIA_ROOT+'/'+'phone.txt',"a")
    if request.POST:
        form = WaitList(request.POST)
        if form.is_valid():
            message = "Name: %s  \r\n Email:%s\r\n" % (
                form.cleaned_data['My_name_is'],
                form.cleaned_data['My_email_is'],			
             
            )
            fileObj.write(form.cleaned_data['My_name_is']+',')

            fileObj.write(form.cleaned_data['My_email_is']+'\n')

            fileObj.close()
            mail_admins('Contact form', message, fail_silently=False)
            if request.is_ajax():
                return render(request, 'thanks.html')
            else:
                return redirect('thanks')
    else:
        form = WaitList()

    return render(request, 'homepage.html', {'form':form})



#TRANSACTION
@login_required
def main_home(request):
	url='/%s/alltrans'% request.user.username  
	return HttpResponseRedirect(url)
	
@login_required
def searchpage(request, username,form_class=SearchForm):
	queryset=Transaction.objects.all().order_by('-created')
	search_form=SearchForm(request.REQUEST)
	if search_form.is_valid():
		search_variable1=search_form.cleaned_data.get('sender_country',None)
		search_variable2=search_form.cleaned_data.get('receiver_country',None)
		search_variable3=search_form.cleaned_data.get('min_amount',None)
		search_variable4=search_form.cleaned_data.get('max_amount',None)

		if search_variable1:
			country_query = Country.objects.filter(countryname__iexact=search_variable1)
			bank_query = Bank.objects.filter(bankcountry=country_query)
			mybankaccount_query = MyBankAccount.objects.filter(bank=bank_query)
			queryset=queryset.filter(sender=mybankaccount_query)
			
			
		if search_variable2:
			#import pdb
			#pdb.set_trace()
			country_query = Country.objects.filter(countryname__iexact=search_variable2)
			bank_query = Bank.objects.filter(bankcountry=country_query)
			recipientbankaccount_query = RecipientBankAccount.objects.filter(bank=bank_query)
			queryset=queryset.filter(receiver=recipientbankaccount_query)
		
		if search_variable3:
			queryset=queryset.filter(amount__gte=search_variable3)
		if search_variable4:
			queryset=queryset.filter(amount__lte=search_variable4)
	
	
	return object_list(request,
	                  queryset=queryset,
	                  template_name="main/alltrans.html",
	                  extra_context={'search_form':search_form},
	                  paginate_by=200,
	                  page=request.GET.get('page',1))
	
	
def user_public_past_trans(request,createdby):
	sender=User.objects.filter(username=createdby)
	queryset=Transaction.objects.filter(createdby=sender)	
	return object_list(request,
	                  queryset=queryset,
	                  template_name="main/public_transaction_list.html",
	                  paginate_by=200,
	                  page=request.GET.get('page',1))


#TRANSACTION CREATE,EDIT AND ACCEPT
@login_required
def transfer(request):
	if  MyBankAccount.objects.filter(createdby=request.user).exists():                                                                                                                  
		url = '/%s/trans/create' % request.user.username
	else:
		url = '/%s/mybank/add' % request.user.username   
	return HttpResponseRedirect(url)
	
		
class TransactionCreateView(CreateView):
	form_class = TransactionForm
	template_name = 'main/transfer.html'
	success_url = 'success'
	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(TransactionCreateView, self).dispatch(*args, **kwargs)
	def get_form_kwargs(self, **kwargs):
		kwargs = super(TransactionCreateView, self).get_form_kwargs(**kwargs)
		kwargs['sender'] = self.request.user
		kwargs['createdby']=self.request.user
		return kwargs
	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.createdby = self.request.user
		self.object.save()
		return super(TransactionCreateView, self).form_valid(form)	
					
@login_required
def transaction_created(request, username, public_profile_field=None,template_name='main/transaction_created.html',
							extra_context=None):
					return render(request, template_name)	
@login_required
def trans_edit(request,objectid):
	url = '/%s/trans/edit/%s' % ( request.user.username, objectid)
	return HttpResponseRedirect(url)
@login_required
def trans_edited(request, username, public_profile_field=None,template_name='main/trans_edited.html',
								extra_context=None):
		return render(request, template_name)	
class TransactionUpdateView(UpdateView):
	
	form_class = TransactionForm
	template_name='main/trans_edit.html'
	success_url='success'
	#@method_decorator(login_required)
	def get(self, request, *args, **kwargs):
		self.object = self.get_object()
		#self.check_permission(request.user, self.object)
		return super(TransactionUpdateView, self).get(request, *args, **kwargs)
	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		#self.check_permission(request.user, self.object)
		return super(TransactionUpdateView, self).post(request, *args, **kwargs)
		
class PostTransactionUpdateView(UpdateView):
	
	form_class = PostTransactionForm
	template_name='main/trans_edit.html'
	success_url='success'
	#@method_decorator(login_required)
	def get(self, request, *args, **kwargs):
		self.object = self.get_object()
		#self.check_permission(request.user, self.object)
		return super( PostTransactionUpdateView, self).get(request, *args, **kwargs)
	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		#self.check_permission(request.user, self.object)
		return super(PostTransactionUpdateView, self).post(request, *args, **kwargs)		
@login_required
def rtrans_accept(request,objectid):
	url = '/%s/trans/accept/%s' % ( request.user.username, objectid)
	return HttpResponseRedirect(url)
@login_required
def reverse_trans_accept(request, username, id,public_profile_field=None,template_name='main/reverse_trans_accepted.html',extra_context=None):								
		rev_tran=ReverseTransaction.objects.get(id=id)
		rev_tran.status='Y'	
		rev_tran.save()
		ot=Transaction.objects.get(id=rev_tran.org_tran.id)
		ot.status='Y'
		ot.save()
		
		return render(request, template_name)
				
#REVERSE TRANSACTION		
@login_required
def reverse_transfer(request,id):
	if  MyBankAccount.objects.filter(createdby=request.user).exists():                                                                                                                  
		url = '/%s/reverse_trans/%s/create' % (request.user.username,id)
	else:
		url = '/%s/mybank/add' % request.user.username   
	return HttpResponseRedirect(url)
	
class ReverseTransactionCreateView(CreateView):
	form_class = ReverseTransactionForm
	template_name = 'main/reverse_transfer.html'
	success_url = 'success'
	context_object_name = "trans"

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(ReverseTransactionCreateView, self).dispatch(*args, **kwargs)
	def get_initial(self):
		initial = super(ReverseTransactionCreateView, self).get_initial()
		# Copy the dictionary so we don't accidentally change a mutable dict
		initial = initial.copy()
		org_tran=Transaction.objects.get(id=self.kwargs['id'])
		
		initial['amount'] = org_tran.amount

		return initial
	def get_form_kwargs(self, **kwargs):
		kwargs = super(ReverseTransactionCreateView, self).get_form_kwargs(**kwargs)
		kwargs['sender'] = self.request.user
		kwargs['createdby']=self.request.user
		return kwargs
	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.createdby = self.request.user
		self.object.org_tran=Transaction.objects.get(id=self.kwargs['id'])
		self.object.save()
		return super(ReverseTransactionCreateView, self).form_valid(form)		
	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(ReverseTransactionCreateView, self).get_context_data(**kwargs)
		org_tran=Transaction.objects.get(id=self.kwargs['id'])
		context['id']=org_tran
		return context	
@login_required
def reverse_transaction_created(request, username,id, public_profile_field=None,template_name='main/reverse_transaction_created.html',
							extra_context=None):
					return render(request, template_name)

def reverse_trans_history(request):
	url = '/%s/reverse_trans' % request.user.username
	return HttpResponseRedirect(url)
	
		
		
	
#TRANSACT-list all existing transactions-this page is shown in profile section
def trans_history(request):
	url = '/%s/trans' % request.user.username
	return HttpResponseRedirect(url)

	
def user_private_past_trans(request,username):
	sender=User.objects.filter(username=username)
	queryset=Transaction.objects.filter(createdby=sender)
	
	return object_list(request,
	                  queryset=queryset,
	                  template_name="main/transaction_list.html",
	                  paginate_by=200,
	                  page=request.GET.get('page',1))
	
def user_private_past_reverse_trans(request,username):
	sender=User.objects.filter(username=username)
	queryset=ReverseTransaction.objects.filter(createdby=sender)
	return object_list(request,
	                  queryset=queryset,
	                  template_name="main/reverse_transaction_list.html",
	                  paginate_by=200,
	                  page=request.GET.get('page',1))		


#ACCOUNT MANAGEMENT	
@login_required
def mybank_manage(request):
	url = '/%s/mybank/manage' % request.user.username
	return HttpResponseRedirect(url)

@login_required
def manage_mybank(request, username, public_profile_field=None,template_name='main/mybankaccount_list.html',
		extra_context=None):
	return render(request, template_name)
		
@login_required
def mybank_add(request):
	url = '/%s/mybank/add' % request.user.username
	return HttpResponseRedirect(url)
	
@login_required
def mybank_edit(request,objectid):
	url = '/%s/mybank/edit/%s' % ( request.user.username, objectid)
	return HttpResponseRedirect(url)	
@login_required
def mybank_delete(request,objectid):
	url = '/%s/mybank/delete/%s' % ( request.user.username, objectid)
	return HttpResponseRedirect(url)

@login_required
def mybank_added(request, username, public_profile_field=None,template_name='main/mybankaccount_created.html',
					extra_context=None):
	return render(request, template_name)
	
class BankAccountCreateView(CreateView):
	form_class = BankAccountForm
	template_name='main/mybankaccount_new.html'
	success_url='success'
	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.createdby = self.request.user
		self.object.save()
		return super(BankAccountCreateView, self).form_valid(form)	
class BankAccountUpdateView(UpdateView):

	form_class = BankAccountForm
	template_name='main/mybankaccount_edit.html'
	success_url='success'
	def get(self, request, *args, **kwargs):
		self.object = self.get_object()
		return super(BankAccountUpdateView, self).get(request, *args, **kwargs)
	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		return super(BankAccountUpdateView, self).post(request, *args, **kwargs)
		
class BankAccountDeleteView(DeleteView):
	form_class = BankAccountForm
	success_url='success'
	def get(self, request, *args, **kwargs):
		self.object = self.get_object()		
		return super(BankAccountDeleteView, self).get(request, *args, **kwargs)
	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()
		self.object.delete()
		return HttpResponseRedirect(self.get_success_url())
		
	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.createdby = self.request.user
		self.object.save()
		return super(BankAccountCreateView, self).form_valid(form)
@login_required
def mybank_edited(request, username, public_profile_field=None,template_name='main/mybankaccount_edited.html',
							extra_context=None):
	return render(request, template_name)
@login_required
def mybank_deleted(request, username, public_profile_field=None,template_name='main/mybankaccount_deleted.html',
								extra_context=None):
	return render(request, template_name)			


#ACCOUNT MANAGEMENT-RECIPIENT			
@login_required
def recipient_manage(request):
	url = '/%s/recipient/manage' % request.user.username
	return HttpResponseRedirect(url)

@login_required
def manage_recipient(request, username, public_profile_field=None,template_name='main/recipientbankaccount_list.html',
		extra_context=None):
	return render(request, template_name)	
@login_required
def recipient_add(request):
	url = '/%s/recipient/add' % request.user.username
	return HttpResponseRedirect(url)
@login_required
def recipient_added(request, username, public_profile_field=None,template_name='main/recipient_created.html',
				extra_context=None):
		return render(request, template_name)

class RecipientBankAccountCreateView(CreateView):
	form_class = RecipientBankAccountForm
	template_name='main/recipientbankaccount_new.html'
	success_url='success'
	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(RecipientBankAccountCreateView, self).dispatch(*args, **kwargs)
	def get_form_kwargs(self, **kwargs):
		kwargs = super(RecipientBankAccountCreateView, self).get_form_kwargs(**kwargs)
		return kwargs
	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.createdby = self.request.user
		self.object.save()
		return super(RecipientBankAccountCreateView, self).form_valid(form)

@login_required
def recipientbank_edit(request,objectid):
	url = '/%s/recipientbank/edit/%s' % ( request.user.username, objectid)
	return HttpResponseRedirect(url)
@login_required
def recipientbank_edited(request, username, public_profile_field=None,template_name='main/recipientbankaccount_edited.html',
								extra_context=None):
		return render(request, template_name)	
class RecipientBankAccountUpdateView(UpdateView):
	
	form_class = RecipientBankAccountForm
	template_name='main/recipientbankaccount_edit.html'
	success_url='success'
	def get(self, request, *args, **kwargs):
		self.object = self.get_object()
		return super(RecipientBankAccountUpdateView, self).get(request, *args, **kwargs)
	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		return super(RecipientBankAccountUpdateView, self).post(request, *args, **kwargs)
		
@login_required
def recipientbank_delete(request,objectid):
	url = '/%s/recipientbank/delete/%s' % ( request.user.username, objectid)
	return HttpResponseRedirect(url)
	
	
class RecipientBankAccountDeleteView(DeleteView):
	form_class = RecipientBankAccountForm
	success_url='success'
	def get(self, request, *args, **kwargs):
		self.object = self.get_object()
		return super(RecipientBankAccountDeleteView, self).get(request, *args, **kwargs)
	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()
		self.object.delete()
		return HttpResponseRedirect(self.get_success_url())
	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.createdby = self.request.user
		self.object.save()
		return super(RecipientBankAccountCreateView, self).form_valid(form)
				
@login_required
def recipientbank_deleted(request, username, public_profile_field=None,template_name='main/recipientbankaccount_deleted.html',
										extra_context=None):
	return render(request, template_name)
	

