
from scrapy.spiders import CrawlSpider
import os
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, Request
import mysql.connector
import json
from scrapy import Selector
from w3lib.url import add_or_replace_parameter, url_query_cleaner

class Domain3Spider(scrapy.Spider):
    name = 'gold-club-direct.sjv.io'

    def parse(self, response):
        # Your scraping logic for domain 2
        
        price = response.css('.summary.entry-summary .product-main-price-wrap .woocommerce-Price-amount.amount bdi::text').get(default='').strip()
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

class GoldclubdirectSpider(scrapy.Spider):
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
        'DOWNLOAD_DELAY': 5,  # Adjust download delay as needed
        'CONCURRENT_REQUESTS_PER_DOMAIN': 5,  # Limit concurrent requests to avoid triggering anti-bot mechanisms
        'COOKIES_ENABLED': True,
        'AUTOTHROTTLE_ENABLED': True,
        'RETRY_TIMES': 2,  # Retry failed requests
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 400, 403, 404],
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_useragents.downloadermiddlewares.useragents.UserAgentsMiddleware': 500,
        }
    }
    name = "goldclubdirect"
    # allowed_domains = ["goldclubdirect.com", "gold-club-direct.sjv.io"]
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
        cursor.execute("SELECT id, link, product_name, dealer FROM findbull WHERE dealer LIKE '%GoldClub Direct%'")  # Assuming you have an ID column
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        for row in rows:
            yield scrapy.Request(url=row[1], meta={'handle_httpstatus_list': [301],'id': row[0], 'product_name': row[2], 'dealer': row[3]}, callback=self.parse_domain1,  # Add a referer header to simulate the source URL
                dont_filter=True)
    def parse_domain1(self, response):
        # print(response)
        yield from Domain3Spider().parse(response)
    #     if response.status == 301 or response.status == 302:
    #         # If the response is a redirect, follow it
    #         redirect_url = response.headers.get('Location')
    #         yield scrapy.Request(url=redirect_url, meta=response.meta, callback=self.parse_redirected_url)
    #     else:
    #         # If not a redirect, proceed with parsing the original response
    # def parse_redirected_url(self, response):
    # # Handle parsing of the redirected URL
    #     yield from Domain3Spider().parse(response)
