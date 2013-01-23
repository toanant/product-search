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
kitaab= db.kitaab

#es = ElasticSearch("http://localhost:9200")

@celery.task
def fetch_attributes(url):
    attrs = {}
    l = []
    detail = {}
    attrs["url"] = url

    # create a request object
    r = requests.get(url)

    if r.status_code == 200:
        # create a pyquery document from response body of above request
        d = pq(r.text)


### Book Details table Content will be stored in detail{}:
	table = d(".fk-specs-type2")
	for t in table.children():
		l.append(t.text_content().strip().splitlines())
		i = 1
        b = len(l)
        while(i < (b-1)):
			try:
				detail[l[i][0]] = l[i][1].strip()
				i +=1
			except IndexError:
				i = b +1

        

	attrs["price"] = d("meta[itemprop=\"price\"]").attr("content")
        attrs["name"] = d("h1[itemprop=\"name\"]").attr("title")
        try:
		attrs["ratingValue"] = float(d("meta[itemprop=\"ratingValue\"]").attr("content"))
	except TypeError:
		attrs["ratingValue"] = 'Not Rated'
        try:
		attrs["ratingCount"] = int(d("span[itemprop=\"ratingCount\"]").text())
	except TypeError:
		attrs["ratingCount"] = 'None'
        attrs["keywords"] =  d("meta[name=\"Keywords\"]").attr("content").split(",")


	attrs['Publisher'] = detail['Publisher']
	attrs['Publication Year']= detail['Publication Year']
	attrs['ISBN-13']= detail['ISBN-13']
	attrs['ISBN-10'] = detail['ISBN-10']
	try:
		attrs['Language'] = detail['Language']
	except KeyError:
		attrs['Language'] = 'None'
	try:
		attrs['Binding'] = detail['Binding']
	except KeyError:
		attrs['Binding'] = 'None'
	try:
		attrs['Number of Pages'] = detail['Number of Pages']
	except KeyError:
		attrs['Number of Pages'] = 'None'


      # es.index("flipkart", "books", attrs)
        ISBN = str(detail['ISBN-13'])
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
		attrs['Infibeam'] = 'None'

	## for Crossword website Price
	if d['Crossword']:
		try:
			attrs['Crossword'] = d['Crossword']("span[class=\"variant-final-price\"]").text().strip('R')
		except AttributeError:
			attrs['Crossword'] = d['Crossword']("span[class=\"variant-final-price\"]").text()
	else:
		 attrs['Crossword'] = 'None'
	
	## for Homeshop18 website Price
	if d['Homeshop18']:
		try:
			attrs['Homeshop18'] = d['Homeshop18']("span[class=\"pdp_details_hs18Price\"]").text().strip('Rs.')
		except AttributeError:
			attrs['Homeshop18'] = d['Homeshop18']("span[class=\"pdp_details_hs18Price\"]").text()
	else:
		attrs['Homeshop18']  =  'None'

	## for Bookadda website Price
	if d['Bookadda']:
		try:
			attrs['Bookadda'] =  d['Bookadda']("span[class=\"actlprc\"]").text().strip('Rs.')
		except AttributeError:
			attrs['Bookadda'] =  d['Bookadda']("span[class=\"actlprc\"]").text()

	else:
		attrs['Bookadda'] =  'None'
	## for rediff book website
	if d['Rediffbook']:
		try:
			attrs['Rediffbook'] = d['Rediffbook']("div[class=\"proddetailinforight\"]").text().split()[2]
		except IndexError:
			attrs['Rediffbook'] = d['Rediffbook']("div[class=\"proddetailinforight\"]").text()
	else:
		attrs['Rediffbook'] =  'None'  
 

	kitaab.insert(attrs)

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
