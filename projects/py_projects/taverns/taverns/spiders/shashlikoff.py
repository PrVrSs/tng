import scrapy
import re
from urllib import parse
from taverns.items import TavernsItem


class Shashlikoff(scrapy.Spider):

    name = "shashlikoff"

    def start_requests(self):
        urls = [
            'http://www.shashlikoff.com/catalog/',
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        catalogs: list = response.xpath("//div[@class='z_order-section-list']/a/@href").extract()

        for catalog in catalogs:
            url: str = parse.urljoin(response.url, catalog)
            yield scrapy.Request(url=url, callback=self.parse_catalog_page)

    def parse_catalog_page(self, response):
        tavern_item: TavernsItem = TavernsItem()
        # Найти адекватный способ понимать, что у некоторых объектов нет всех полей
        base_url: str = parse.urlparse(response.url).netloc
        tavern_item['base_url'] = response.url
        tavern_item['title'] = list(map(lambda args: re.sub(r'<[^>]*?>', '', args), response.xpath("//section[@class='row hits-items']/article/h3/a").extract()))
        tavern_item['desc'] = list(map(lambda args: re.sub(r'<[^>]*?>', '', args), response.xpath("//section[@class='row hits-items']/article/p[@class='item-description']").extract()))
        tavern_item['price'] = list(map(lambda args: re.sub(r'<[^>]*?>', '', args), response.xpath("//section[@class='row hits-items']/article/p[@class='item-price']/span").extract()))
        tavern_item['image'] = list(map(lambda args: base_url + args, response.xpath("//section[@class='row hits-items']/article/a/picture/img/@src").extract()))

        yield tavern_item
