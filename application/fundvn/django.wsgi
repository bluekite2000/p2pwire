import os
import sys

sys.path.append('/srv/www/fundvn.com/application/cookie')
sys.path.append('/srv/www/fundvn.com/application/')

os.environ['PYTHON_EGG_CACHE'] = '/srv/www/fundvn/.python-egg'

os.environ['DJANGO_SETTINGS_MODULE'] = 'cookie.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
