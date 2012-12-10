from flask import Flask, render_template
app = Flask(__name__)

from pyelasticsearch import ElasticSearch

import json

es = ElasticSearch("http://localhost:9200/")

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/search/<query>")
@app.route("/search/<query>/<limit>")
@app.route("/search/<query>/<start>/<limit>")
def search(query=None, start = 0, limit = 50):
    if query:
        res = es.search("name:%s" % (query), index="flipkart", es_from = start, es_size = limit)
        #return json.dumps(res)
        products = res["hits"]["hits"]
        return render_template("search.html", products=products)
    return "Query can't be empty."

if __name__ == "__main__":
    app.run(debug=True)
