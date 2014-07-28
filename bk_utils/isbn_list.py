import requests
from pyquery import PyQuery as pq
from lxml import etree

# from flipkart_settings import *
from web_setting import *
from celery import Celery

from pymongo import MongoClient

#from pyelasticsearch import ElasticSearch

celery = Celery("tasks", broker="amqp://guest@localhost")

# connect to mongodb database
connection = MongoClient()
db = connection.abhi
pustak= db.pustak

@celery.task
def get_isbn(count, start =0):
    isbn = []
    if (count !=0):
        url = "%s/computers-internet-books-1171?response-type=json&inf-start=%d" % (BASE_URL, start)

    r = requests.get(url)
    json = r.json()

    if r.status_code == 200:
	count = pq(json["count"])
	d = pq(json["html"])
        for a in d:
		urls.append("%s%s" % (BASE_URL, d(a).attr("href")))

    res = {}
    res["urls"] = urls
    res["datacount"] = json["data"]["datacount"]
    res["more_url"] = "%s%s" % (BASE_URL, json["data"]["more_url"])
    res["start"] = json["data"]["start"]

    return res

