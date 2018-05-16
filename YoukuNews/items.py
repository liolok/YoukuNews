# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class YoukuItem(Item):
    # # define the fields for your item here like:
    # # name = Field()

    # 基本信息, 将由 spider.parse_basic() 解析
    url = Field()           # 页面链接
    title = Field()         # 标题
    thumb = Field()         # 缩略图链接
    time = Field()          # 时长
    statplay = Field()      # 播放量
    statcomment = Field()   # 评论数

    # 详细信息, 将由 spider.parse_detail() 解析
    subtitle = Field()      # 副标题
    category = Field()      # 分类
    channel_name = Field()  # 频道名称
    channel_link = Field()  # 频道链接

    # pass
