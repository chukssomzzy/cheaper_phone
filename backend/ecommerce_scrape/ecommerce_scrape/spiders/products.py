import scrapy


class ProductsSpider(scrapy.Spider):
    name = "products"
    allowed_domains = ["www.konga.com"]
    start_urls = ["https://www.konga.com"]

    def parse(self, response):
        pass
