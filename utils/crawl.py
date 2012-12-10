from tasks import *

def crawl(category="laptops"):

    if category not in CATEGORIES:
        raise InvalidCategoryException


    res = get_urls(category=category)

    for u in res["urls"]:
        fetch_attributes.delay(u)

    i = 0
    while True:
        i += 1
        print i, res["datacount"], res["start"]
        if res["start"] != 0 and res["more_url"]:
            res = get_urls(more_url=res["more_url"])
            for u in res["urls"]:
                fetch_attributes.delay(u)
        else:
            break
                

crawl()
