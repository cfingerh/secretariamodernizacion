import sys
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")
os.environ['DJANGO_SETTINGS_MODULE'] = 'conf.settings'
application = get_wsgi_application()

from django.db.models import Sum, Count, F, Avg
from base.models import *


import json
