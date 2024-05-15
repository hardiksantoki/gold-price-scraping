from scrapy.spiders import CrawlSpider
import os
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, Request
import mysql.connector
import json
from scrapy import Selector
from w3lib.url import add_or_replace_parameter, url_query_cleaner

class Domain4Spider(scrapy.Spider):
    name = 'www.silver.com'

    def parse(self, response):
        # Your scraping logic for domain 2
        price = response.css('.main_cont .product_top .product_topRgt .price_tbl tbody tr td:nth-child(2) big::text').get(default='').strip()
        id = response.meta['id']
        product_name = response.meta['product_name']
        dealer = response.meta['dealer']
        yield {
            'id': id,
            'name': product_name,
            'dealer': dealer,
            'price': price
        }
        pass


class SilverComSpider(scrapy.Spider):
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
        'DOWNLOAD_DELAY': 5,  
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,  
        'COOKIES_ENABLED': True,
        'AUTOTHROTTLE_ENABLED': True,
        'RETRY_TIMES': 2,  # Retry failed requests
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 400, 403, 404],
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_useragents.downloadermiddlewares.useragents.UserAgentsMiddleware': 500,
        }
    }
    name = "Silver_com"
    allowed_domains = ["www.silver.com"]
    # start_urls = ["https://www.silver.com/"]
    def start_requests(self):
        # rules = (
        #     Rule(LinkExtractor(restrict_css=products_css), callback='parse'),
        # )
        # start_urls = ["https://goldclubdirect.com/"]
        conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='gold'
            )
        cursor = conn.cursor()
        cursor.execute("SELECT id, link, product_name, dealer FROM findbull WHERE dealer LIKE '%Silver.com%'")  # Assuming you have an ID column
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        for row in rows:
            yield scrapy.Request(url=row[1], meta={'id': row[0], 'product_name': row[2], 'dealer': row[3]}, callback=self.parse_domain1)

    def parse_domain1(self, response):
        # Handle response for domain 1
        yield from Domain4Spider().parse(response)
