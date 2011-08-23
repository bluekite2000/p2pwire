from django.http import HttpResponseRedirect
from django import template
register = template.Library()

from django.contrib.auth.forms import AuthenticationForm

@register.inclusion_tag('registration/login_error.html', takes_context=True)
def form_login(context):
    return { 'form': AuthenticationForm() }
    #request=context['request']
    #user = context['user']
    #if user.is_authenticated():
        #url_address = '/%s/recipient/addr' % request.user.username
        #return HttpResponseRedirect(url_address)
    
    #else: 
        #return { 'form': AuthenticationForm() }