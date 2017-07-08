#!/usr/bin/env python

import json
import datetime
from dateutil.tz import tzlocal
from pprint import pprint
from elasticsearch import Elasticsearch

indexname = "darkskynest"
doc_type = "darkskynest"
darkskyindex = "darksky-*"
nestindex = "nest-*"
elastichost='localhost:9200'

dualdata = {}

es = Elasticsearch(elastichost)

now = datetime.datetime.now(tzlocal())

month = now.strftime("%m")
year = now.strftime("%Y")
index = indexname + "-" + year + "-" + month

with open('getnest.json') as json_data:
    nestjson = json.load(json_data)

with open('getdarksky.json') as json_data:
    darkskyjson = json.load(json_data)

nestres = es.search(index=nestindex, body=nestjson)
darkskyres = es.search(index=darkskyindex, body=darkskyjson)

dualdata['nesttemp'] = nestres['aggregations']['nesttemp']['value']
dualdata['nesthumidity'] = nestres['aggregations']['nesthumidity']['value']
dualdata['darkskytemp'] = darkskyres['aggregations']['darkskytemp']['value']
dualdata['darkskyhumidity'] = darkskyres['aggregations']['darkskyhumidity']['value'] * 100
dualdata['tempdifference'] = dualdata['darkskytemp'] - dualdata['nesttemp']
dualdata['humiditydifference'] = dualdata['darkskyhumidity'] - dualdata['nesthumidity']
dualdata['timestamp'] = now

es.index(index=index, doc_type=doc_type, id=now, body=dualdata)
