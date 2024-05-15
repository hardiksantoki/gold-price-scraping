import scrapy


class SilverComSpider(scrapy.Spider):
    name = "Silver_com"
    allowed_domains = ["www.silver.com"]
    start_urls = ["https://www.silver.com/"]

    def parse(self, response):
        pass
