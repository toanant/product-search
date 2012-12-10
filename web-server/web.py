from flask import Flask, render_template, request
from pyelasticsearch import ElasticSearch
import json
from datetime import datetime

from flask.ext.paginate import Pagination

app = Flask(__name__)
es = ElasticSearch("http://localhost:9200/")

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/search/", methods=["GET"])
def search():
    search = True
    _started_at = datetime.now()
    query = request.args.get("q")
    start = request.args.get("start")
    limit = request.args.get("limit")
    page = request.args.get("page")
    
    if query:
        start = 0 if not start else int(start)
        limit = 10 if not limit else int(limit)
        if page:
            page = int(page)
            start = (page-1)*limit

        d = {
                "sort": {
                    "ratingCount": {"order": "desc"},
                    "ratingValue": {"order": "desc"},
                },
                "query": {
                    "term": {
                        "name": query.lower(),
                     },
                }
            }

        #return json.dumps(d)
        res = es.search(d, index="flipkart", es_from = start, es_size = limit)
        total = res["hits"]["total"]
        pagination = Pagination(found = total, search = search, total=total, per_page = limit)

        #return json.dumps(res)
        products = res["hits"]["hits"]
        _ended_at = datetime.now()
        return render_template("search.html",
                               products=products,
                               time_taken=(_ended_at - _started_at).total_seconds(),
                               pagination=pagination,
                               start = start,
                               count = total
                               )
    return "Query can't be empty."

if __name__ == "__main__":
    app.run(debug=True)
