# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class VideoItem(Item):      # 视频信息
    # 基本信息, 将由 spider.parse_basic() 解析
    url = Field()           # 页面链接
    vid = Field()           # 唯一识别码
    title = Field()         # 标题
    thumb_url = Field()     # 缩略图下载链接(由ThumbPipeline下载)
    thumb_path = Field()    # 缩略图本地路径(由ThumbPipeline填入)
    time = Field()          # 时长
    stat_play = Field()     # 播放量
    stat_cmt = Field()      # 评论量

    # 详细信息, 将由 spider.parse_detail() 解析
    subtitle = Field()      # 副标题
    category = Field()      # 分类
    channel_name = Field()  # 频道名称
    channel_link = Field()  # 频道链接

    # 文件信息, 将由 spider.parse_file() 解析
    file_urls = Field()     # 分段视频下载链接列表(由FilesPipeline下载)
    file_paths = Field()    # 分段视频本地路径列表(由FilesPipeline填入)

    # 评论信息, 将由 spider.parse_comment() 解析
    comment_list = Field()  # 所有评论列表, 嵌套若干 CommentItem
    comment_num = Field()   # 评论数目
    comment_hot = Field()   # 热评id列表


class CommentItem(Item):    # 评论信息
    id = Field()            # 唯一识别码
    time = Field()          # 发布时间戳
    user = Field()          # 发布用户ID
    content = Field()       # 评论内容
    num_up = Field()        # 点赞数
    num_down = Field()      # 点踩数
    num_reply = Field()     # 回复数
