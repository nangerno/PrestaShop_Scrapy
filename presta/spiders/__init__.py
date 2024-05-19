# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
from .index import QuotesSpider
my_instance = QuotesSpider()
my_instance.start_requests()