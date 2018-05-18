# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html#write-items-to-mongodb
# The main point of this example is to show \
# how to use from_crawler() method and how to clean up the resources properly.

from pymongo import MongoClient


class YoukunewsPipeline(object):
    collection_name = 'VideoInfo'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri  # 统一资源标识符
        self.mongo_db = mongo_db  # 数据库名称

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # 对集合(collection)插入一个文档(document)
        self.db[self.collection_name].insert_one(dict(item))
        return item
