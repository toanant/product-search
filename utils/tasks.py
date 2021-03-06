import requests
from pyquery import PyQuery as pq
from lxml import etree

from flipkart_settings import *
from celery import Celery

from pymongo import MongoClient

from pyelasticsearch import ElasticSearch

celery = Celery("tasks", broker="amqp://guest@localhost")

# connect to mongodb database
connection = MongoClient()
db = connection.abhi
products= db.products

es = ElasticSearch("http://localhost:9200")

@celery.task
def fetch_attributes(url):
    attrs = {}

    attrs["url"] = url

    # create a request object
    r = requests.get(url)

    if r.status_code == 200:
        # create a pyquery document from response body of above request
        d = pq(r.text)

        attrs["price"] = d("meta[itemprop=\"price\"]").attr("content")
        attrs["name"] = d("h1[itemprop=\"name\"]").attr("title")
        attrs["ratingValue"] = float(d("meta[itemprop=\"ratingValue\"]").attr("content"))
        attrs["ratingCount"] = int(d("span[itemprop=\"ratingCount\"]").text())
        attrs["keywords"] =  d("meta[name=\"Keywords\"]").attr("content").split(",")

        es.index("flipkart", "products", attrs)
        products.insert(attrs)


def get_urls(more_url = None, category = "laptops", limit = 20, start = 0):
    urls = []
    if more_url:
        url = more_url

    else:
        if category not in CATEGORIES:
            raise InvalidCategoryException

        if limit > MAX_LIMIT:
            raise Exception("Limit can't be more than %d"%(MAX_LIMIT))

        url = "%s/search/getQueryBuilderResults?vertical=%s&limit=%d&start=%d" % (BASE_URL, category, limit, start)

    r = requests.get(url)
    json = r.json()

    if r.status_code == 200:
        d = pq(json["data"]["html"])
        for a in d("a.title"):
            urls.append("%s%s" % (BASE_URL, d(a).attr("href")))

    res = {}
    res["urls"] = urls
    res["datacount"] = json["data"]["datacount"]
    res["more_url"] = "%s%s" % (BASE_URL, json["data"]["more_url"])
    res["start"] = json["data"]["start"]

    return res
