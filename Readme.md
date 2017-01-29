How to use the crawler:

cd website_dir

For eg.

cd brightnest

Run this command
scrapy crawl brightnest_crawler

How to use dynamic IP

list.txt file contains the proxy list

In settings.py inside the crawler dir(brighnest/wikihowto) uncomment the DOWNLOADER_MIDDLEWARES

Please use a working proxies for the crawler to work
