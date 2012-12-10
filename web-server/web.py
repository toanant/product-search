from flask import Flask, render_template, request
app = Flask(__name__)

from pyelasticsearch import ElasticSearch
import json

from datetime import datetime

es = ElasticSearch("http://localhost:9200/")

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/search/", methods=["GET"])
def search():
    _started_at = datetime.now()
    query = request.args.get("q")
    start = request.args.get("start")
    limit = request.args.get("limit")
    
    if query:
        start = 0 if not start else start
        limit = 10 if not limit else limit
        res = es.search("name:%s" % (query), index="flipkart", es_from = start, es_size = limit)
        #return json.dumps(res)
        products = res["hits"]["hits"]
        _ended_at = datetime.now()
        return render_template("search.html", products=products, time_taken=(_ended_at - _started_at).total_seconds())
    return "Query can't be empty."

if __name__ == "__main__":
    app.run(debug=True)
