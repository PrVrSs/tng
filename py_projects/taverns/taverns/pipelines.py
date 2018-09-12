# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from pymongo import IndexModel, ASCENDING
from taverns.items import TavernsItem


class TavernsPipeline(object):

    def __init__(self):
        clinet = pymongo.MongoClient("localhost", 27017)
        db = clinet["tavern"]
        self.PhRes = db["shashlikoff_tavern"]
        idx = IndexModel([('base_url', ASCENDING)], unique=True)
        self.PhRes.create_indexes([idx])
        # if your existing DB has duplicate records, refer to:

    # https://stackoverflow.com/questions/35707496/remove-duplicate-in-mongodb/35711737

    def process_item(self, item, spider):
        if isinstance(item, TavernsItem):
            try:
                self.PhRes.update_one({'base_url': item['base_url']}, {'$set': dict((i, item[i]) for i in item if i != 'base_url')}, upsert=True)
            except Exception:
                pass

        return item
