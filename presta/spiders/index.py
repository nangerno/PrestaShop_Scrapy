from pathlib import Path
from scrapy import Selector
import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    
    def start_requests(self):
        urls = [
            "https://stang-parts.de/en/"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    def parse(self, response):
        print('----1-----')
        url_list = []
        all_catogries = response.css('ul.tree.dhtml').getall()
        all_catogries = ''.join(all_catogries)
        new_selector = Selector(text = all_catogries)
        rlt = new_selector.css('li[id*="cat_id_"]')
        for x in rlt:
            x = str(x)
            pos = x.find('cat_id_')
            if pos > 0:
                if (x[pos+7] >= '0') and (x[pos+7] <= '9'):
                    if (x[pos+8] >= '0') and (x[pos+8] <= '9'):
                        if (x[pos+9] >= '0') and (x[pos+9] <= '9'):
                            x = Selector(text = x)
                            ans = x.css('a::attr(href)').get()
                            url_list.append(ans)
        for page in url_list:
            yield scrapy.Request(url=page, callback=self.getpro)
        # yield scrapy.Request(url='https://stang-parts.de/en/745-body-gaskets', callback=self.getpro)
    def getpro(self, response):
        print("----2----")
        all_products = response.css('#products div.product-right h3.product-title a::attr(href)').getall()
        print(len(all_products))
        # yield {
        #     'products': all_products
        # }
        # yield scrapy.Request(url='https://stang-parts.de/en/interior/9122-front-seat-frame-assembly-65-67-lh.html', callback=self.detail)
        for page in all_products:
            yield scrapy.Request(url=page, callback=self.detail)
    def detail(self, response):
        print("-------3-------")
        url = response.request.url
        name = response.css('h1.product_name[itemprop="name"]::text').get()
        reference = response.css('section.product-reference span::text').get()
        brand = response.css('a.editable span::text').get()
        # description = response.css('#product-description-short-31 em::text').get()
        price = response.css('div.current-price span.price::text').get()
        availability = response.css('span#product-availability::text').getall()
        availability_text = ''.join(availability).strip()
        yield {
            'url': url,
            'name': name,
            'refrence': reference,
            'brand': brand,
            # 'description': description,
            'current price': price,
            'availability': availability_text
        }

