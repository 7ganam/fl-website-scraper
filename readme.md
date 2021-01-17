to run first install scrapy
run this command in the same dir as scrapy.cfg: scrapy crawl fl_spider1 -L WARNING -o output.csv
results will be saved in the output.csv file
the currency data was fetched from :
http://www.floatrates.com/json-feeds.html
U.S. Dollar (USD) JSON Feed
I added the usd entry manually
(to be changed later to use a dynamic api)
