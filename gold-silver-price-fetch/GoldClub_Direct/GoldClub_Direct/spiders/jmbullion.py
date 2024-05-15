import scrapy
import mysql.connector
from w3lib.url import url_query_cleaner


# class Domain1Spider(scrapy.Spider):
#     name = 'jmbullion.com'
    # rules = (
    #     # Rule(LinkExtractor(restrict_css=listings_css, tags=('link', 'a')), callback='_parse'),
    #     Rule(LinkExtractor(restrict_css=products_css), callback='parse'),
    # )




class JmbullionSpider(scrapy.Spider):
    name = "jmbullion"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
        'DOWNLOAD_DELAY': 5,  
        'CONCURRENT_REQUESTS_PER_DOMAIN': 5,  
        'COOKIES_ENABLED': False,
        'AUTOTHROTTLE_ENABLED': True,
        # 'FEED_FORMAT': 'json', 
        # 'FEED_URI': 'price_output.json',  
        'RETRY_TIMES': 2,  
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 400, 403, 404],
    }
    # allowed_domains = ["www.jmbullion.com"]
    # start_urls = ["https://www.jmbullion.com/"]

    def start_requests(self):
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='gold'
        )
        cursor = conn.cursor()
        cursor.execute("SELECT id, link, product_name, dealer FROM findbull WHERE dealer LIKE '%JM Bullion%'")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        for row in rows:
            yield scrapy.Request(
                url=row[1],
                meta={'id': row[0], 'product_name': row[2], 'dealer': row[3]},
                callback=self.parse_jm
            )

    # def parse_domain1(self, response):
    #     # Handle response for domain 1
    #     yield from Domain1Spider().parse(response)
    def parse_jm(self, response):
        price = [value.strip() for value in response.css(".product2col .product-detail-region .product-detail-right .payment-section .payment-inner table tbody tr td:nth-child(2)::text").getall() if value.strip()]
        id = response.meta['id']
        product_name = response.meta['product_name']
        dealer = response.meta['dealer']
        yield {
            'id': id,
            'name': product_name,
            'dealer': dealer,
            'price': price[0]
        }
        # Your scraping logic for domain 1
        


