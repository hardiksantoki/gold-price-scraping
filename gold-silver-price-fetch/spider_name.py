import scrapy


class SpiderNameSpider(scrapy.Spider):
    name = "spider_name"
    allowed_domains = ["www.silver.com"]
    start_urls = ["https://www.silver.com/"]

    def parse(self, response):
        pass
