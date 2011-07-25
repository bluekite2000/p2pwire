from django import template
register = template.Library()

#this is used to filter bank accounts created by the logged in person
@register.filter
def filter_by_sender_summerize(queryset, user):
	#import pdb
	#pdb.set_trace()
	summary=[]
	totalamount=0
	index=0
	queryset=queryset.filter(createdby=user)
	for trans in queryset:
		totalamount+=trans.amount
		index=index+1
	summary.append(totalamount)
	summary.append(index)
	return summary
	
@register.filter
def filter_by_user(queryset, user):
    """Filter the queryset by (currently logged in) user"""
    return queryset.filter(createdby=user)

#this is used to filter transactions created by the logged in person (ie.sender)
@register.filter
def filter_by_sender(queryset, user):
	"""Filter the queryset by (currently logged in) user"""
	return queryset.filter(createdby=user)
	
#this is used to filter recipients created by the logged in person
@register.filter
def filter_by_creator(queryset, user):
	"""Filter the queryset by (currently logged in) user"""
	return queryset.filter(createdby=user)