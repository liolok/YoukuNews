# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class VideoItem(Item):
    # # define the fields for your item here like:
    # # name = Field()

    # 基本信息, 将由 spider.parse_basic() 解析
    vid = Field()           # 唯一识别码
    url = Field()           # 页面链接
    title = Field()         # 标题
    thumb_url = Field()     # 缩略图链接
    thumb_path = Field()    # 缩略图保存路径
    time = Field()          # 时长
    statplay = Field()      # 播放量
    statcomment = Field()   # 评论量

    # 详细信息, 将由 spider.parse_detail() 解析
    subtitle = Field()      # 副标题
    category = Field()      # 分类
    channel_name = Field()  # 频道名称
    channel_link = Field()  # 频道链接

    # 评论信息, 将由 spider.parse_comment() 解析
    cmt_num = Field()       # 评论数目
    comment = Field()       # 评论列表


class CommentItem(Item):
    id = Field()            # 唯一识别码
    id_user = Field()       # 发送评论用户
    id_parent = Field()     # 父评论
    at_users = Field()      # 对哪些用户发送
    content = Field()       # 评论内容
    time = Field()          # 评论创建时间
    num_up = Field()        # 点赞数
    num_down = Field()      # 点踩数
    num_reply = Field()     # 回复数
