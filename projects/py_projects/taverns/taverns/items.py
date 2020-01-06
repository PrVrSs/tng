# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TavernsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    base_url = scrapy.Field()
    title = scrapy.Field()
    desc = scrapy.Field()
    price = scrapy.Field()
    image = scrapy.Field()
