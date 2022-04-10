import sys
import json
import os
import importlib
import pandas as pd
from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")
os.environ['DJANGO_SETTINGS_MODULE'] = 'conf.settings'
application = get_wsgi_application()

from base.models import *


df = pd.read_excel('datos.xlsx', index_col=0)

raws = []
Raw.objects.all().delete()
for index, row in df.iterrows():
    raw = Raw(codigo_cf=row.codigo_cf, anio=row.medicion, datos=json.loads(row.to_json()))
    raws.append(raw)
    if len(raws) == 1000:
        r = Raw.objects.bulk_create(raws)
        raws = []
        print(Raw.objects.all().count())

r = Raw.objects.bulk_create(raws)
