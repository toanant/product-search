## This urlset contains website:search pattern in dictionary accordingly.
urlset={'Infibeam':'http://www.infibeam.com/Books/search?q=', 'Crossword':'http://www.crossword.in/books/search?q=', 'Homeshop18':'http://www.homeshop18.com/search:', 'Bookadda':'http://www.bookadda.com/general-search?searchkey=', 'Rediffbook':'http://books.rediff.com/book/ISBN:'}

## It contains price-value grabbing to diiferent website 
#priceset={'Infibeam':"("span[class=\"infiPrice amount price\"]").text()", 'Crossword':"("span[class=\"variant-final-price\"]").text().strip('R')", 'Homeshop18':"("span[class=\"pdp_details_hs18Price\"]").text().strip('Rs.')", 'Bookadda':"("span[class=\"actlprc\"]").text().strip('Rs.')", 'Rediffbook':"("div[class=\"proddetailinforight\"]").text().split()[2]"}

