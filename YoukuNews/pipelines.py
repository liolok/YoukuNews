# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html#write-items-to-mongodb
# The main point of this example is to show \
# how to use from_crawler() method and how to clean up the resources properly.

from pymongo import MongoClient
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline


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


class ThumbPipeline(ImagesPipeline):
    # 从item中取出缩略图的url并下载文件
    def get_media_requests(self, item, info):
        yield Request(url=item['thumb_url'], meta={'item': item})

    # 自定义缩略图路径(仅更改命名)
    def file_path(self, request, response=None, info=None):
        item = request.meta['item']  # 接受 get_media_requests 传入的 item
        return "%s - %s.jpg" % (item['vid'],item['title'])  # 返回命名格式

    # 下载完成后, 将缩略图本地路径保存到item中
    def item_completed(self, results, item, info):
        item['thumb_path'] = [x['path'] for ok, x in results if ok][0]
        return item
