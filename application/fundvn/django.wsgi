import os
import sys

sys.path.append('/srv/www/p2pwire.com/application/fundvn')
sys.path.append('/srv/www/p2pwire.com/application/')

os.environ['PYTHON_EGG_CACHE'] = '/srv/www/fundvn/.python-egg'

os.environ['DJANGO_SETTINGS_MODULE'] = 'fundvn.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
