# -*- coding: utf-8 -*-

from scrapy import Spider, Request
from YoukuNews.items import YoukuItem
from re import compile, search

# 预编译正则表达式, 用于解析视频页面详细信息
re_subtitle = compile(r'subtitle\\\" title=\\\"(.+?)\\\">')
re_category = compile(r'irCategory\\\" content=\\\"(.+?)\\\"')
re_channame = compile(r'module_basic_sub.+?alt.+?\\n\s+(.+?)\\')
re_chanlink = compile(r'module_basic_sub.+?(//i\.youku\.com/i/(?:[A-Za-z0-9]+))')


class YoukuSpider(Spider):
    name = 'youku'  # 爬虫唯一识别名
    allowed_domains = ['youku.com']  # 爬取域名范围

    # 从以下三个目录页面开始解析
    def start_requests(self):
        yield Request('http://news.youku.com/index/jrrm', self.parse_basic)  # 今日热门
        yield Request('http://news.youku.com/index/jkjs', self.parse_basic)  # 监控纪实
        yield Request('http://news.youku.com/index/jsqy', self.parse_basic)  # 军事前沿

    # 从目录页面解析视频列表及其基本信息
    def parse_basic(self, response):
        list = []  # 创建视频列表
        for v in response.css('.v'):  # 遍历目录页面
            item = YoukuItem()  # 循环实例化 YoukuItem, 并解析基本信息填入
            item['url'] = v.css('.v-link').xpath('./a/@href') \
                .re_first('(//v.youku.com/v_show/id_(?:[A-Za-z0-9=]+))')
            item['title'] = v.css('.v-link').xpath('./a/@title').extract_first()
            item['thumb'] = v.css('.v-thumb').xpath('./img/@src').re_first('(//.+)')
            item['time'] = v.css('.v-time::text').extract_first()
            item['statplay'] = v.css('.ico-statplay+span::text').extract_first()  # 播放图标后面的文本
            item['statcomment'] = v.css('.ico-statcomment+span::text').extract_first()  # 评论图标后面的文本
            list.append(item)  # 追加视频列表
        for item in list:  # 回调 parse_detail() 对列表中的每个 YoukuItem 的视频页面进行解析
            yield Request(url="https:" + item['url'], meta={'list': item}, callback=self.parse_detail)

    # 从视频页面解析详细信息
    def parse_detail(self, response):
        item = response.meta['list']  # 接收 parse_basic() 传入的 YoukuItem
        source = response.body.decode("utf-8")  # 对源码进行正则匹配
        item['subtitle'] = re_subtitle.search(source).group(1)
        item['category'] = re_category.search(source).group(1)
        item['channel_name'] = re_channame.search(source).group(1)
        item['channel_link'] = "https:" + re_chanlink.search(source).group(1)
        yield item  # 返回填写好的 YoukuItem
