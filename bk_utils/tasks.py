import requests
from pyquery import PyQuery as pq
from lxml import etree

from flipkart_settings import *
from web_setting import *
from celery import Celery

from pymongo import MongoClient

#from pyelasticsearch import ElasticSearch

celery = Celery("tasks", broker="amqp://guest@localhost")

# connect to mongodb database
connection = MongoClient()
db = connection.abhi
books= db.books

#es = ElasticSearch("http://localhost:9200")

@celery.task
def fetch_attributes(url):
    attrs = {}
    l = []
    attrs["url"] = url

    # create a request object
    r = requests.get(url)

    if r.status_code == 200:
        # create a pyquery document from response body of above request
        d = pq(r.text)
        table = d(".fk-specs-type2")
	for t in table.children():
		l.append(t.text_content().strip().splitlines())
	attrs["price"] = d("meta[itemprop=\"price\"]").attr("content")
        attrs["name"] = d("h1[itemprop=\"name\"]").attr("title")
        try:
		attrs["ratingValue"] = float(d("meta[itemprop=\"ratingValue\"]").attr("content"))
	except TypeError:
		attrs["ratingValue"] = 'Not rated'
        attrs["ratingCount"] = int(d("span[itemprop=\"ratingCount\"]").text())
        attrs["keywords"] =  d("meta[name=\"Keywords\"]").attr("content").split(",")
        attrs['Publisher'] = l[1][1].strip()
	attrs['Publication Year']= l[2][1].strip()
	attrs['ISBN-13']= l[3][1].strip()
	attrs['ISBN-10'] = l[4][1].strip()
	attrs['Language'] = l[5][1].strip()
	attrs['Binding'] = l[6][1].strip()
	try:
		attrs['Number of Pages'] = l[7][1].strip()
	except IndexError:
		attrs['Number of Pages'] = 'Not available'


      # es.index("flipkart", "products", attrs)
        ISBN = str(attrs['ISBN-13'])
	d = {}
	for key, value in urlset.items():
		t_url = value + ISBN
		r = requests.get(t_url)	
		if r.status_code == 200:
			key_url = key +'_url'
			attrs[key_url] = t_url
			d[key] = pq(r.text)	
	
	## for Infibeam website Price
	if d['Infibeam']:
		attrs['Infibeam'] = d['Infibeam']("span[class=\"infiPrice amount price\"]").text()
	else:
		attrs['Infibeam'] = 'Not available'

	## for Crossword website Price
	if d['Crossword']:
		try:
			attrs['Crossword'] = d['Crossword']("span[class=\"variant-final-price\"]").text().strip('R')
		except AttributeError:
			attrs['Crossword'] = d['Crossword']("span[class=\"variant-final-price\"]").text()
	else:
		 attrs['Crossword'] = 'Not available'
	
	## for Homeshop18 website Price
	if d['Homeshop18']:
		try:
			attrs['Homeshop18'] = d['Homeshop18']("span[class=\"pdp_details_hs18Price\"]").text().strip('Rs.')
		except AttributeError:
			attrs['Homeshop18'] = d['Homeshop18']("span[class=\"pdp_details_hs18Price\"]").text()
	else:
		attrs['Homeshop18']  =  'Not available'

	## for Bookadda website Price
	if d['Bookadda']:
		try:
			attrs['Bookadda'] =  d['Bookadda']("span[class=\"actlprc\"]").text().strip('Rs.')
		except AttributeError:
			attrs['Bookadda'] =  d['Bookadda']("span[class=\"actlprc\"]").text()

	else:
		attrs['Bookadda'] =  'Not available'
	## for rediff book website
	if d['Rediffbook']:
		attrs['Rediffbook'] = d['Rediffbook']("div[class=\"proddetailinforight\"]").text().split()[2]
	else:
		attrs['Rediffbook'] =  'Not available'  
 

	books.insert(attrs)


def get_urls(more_url = None, category = "books", limit = 20, start = 0):
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
