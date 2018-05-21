# -*- coding: utf-8 -*-

from scrapy import Spider, Request
from YoukuNews.items import YoukuItem, CommentItem
from re import compile
from json import loads

class YoukuSpider(Spider):
    name = 'youku'  # 爬虫唯一识别名
    allowed_domains = ['youku.com']  # 爬取域名范围

    scheme = "https:"  # URL传送协议

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
            link = v.css('.v-link').xpath('./a/@href').re('(//v.youku.com/v_show/id_([A-Za-z0-9]+))')
            item['vid'] = link[1]                   # 链接id字段
            item['url'] = self.scheme + link[0]     # 补全协议类型
            item['title'] = v.css('.v-link').xpath('./a/@title').extract_first()
            item['thumb'] = self.scheme + v.css('.v-thumb').xpath('./img/@src').re_first('//.+')
            item['time'] = v.css('.v-time::text').extract_first()
            item['statplay'] = v.css('.ico-statplay+span::text').extract_first()        # 播放图标后面的文本
            item['statcomment'] = v.css('.ico-statcomment+span::text').extract_first()  # 评论图标后面的文本
            list.append(item)  # 追加视频列表
        for item in list:  # 回调 parse_detail() 对列表中的每个 YoukuItem 的视频页面进行解析
            yield Request(url=item['url'], meta={'list': item}, callback=self.parse_detail)

    # 预编译正则表达式, 用于解析视频页面详细信息
    re_subtitle = compile(r'subtitle\\\" title=\\\"(.+?)\\\">')                         # 副标题
    re_category = compile(r'irCategory\\\" content=\\\"(.+?)\\\"')                      # 分类
    re_channame = compile(r'module_basic_sub.+?alt.+?\\n\s+(.+?)\\')                    # 频道名称
    re_chanlink = compile(r'module_basic_sub.+?(//i\.youku\.com/i/(?:[A-Za-z0-9]+))')   # 频道链接

    # 从视频页面解析详细信息
    def parse_detail(self, response):
        item = response.meta['list']  # 接收 parse_basic() 传入的 YoukuItem
        source = response.body.decode("utf-8")  # 对源码进行正则匹配
        item['subtitle'] = self.re_subtitle.search(source).group(1)
        item['category'] = self.re_category.search(source).group(1)
        item['channel_name'] = self.re_channame.search(source).group(1)
        item['channel_link'] = self.scheme + self.re_chanlink.search(source).group(1)
        # 回调 parse_comment() 对当前 YoukuItem 的评论源码进行解析
        yield Request(url=self.get_cmt_url(item['vid']), meta={'list': item}, callback=self.parse_comment)

    # 从评论源码解析评论内容
    def parse_comment(self,response):
        item = response.meta['list']  # 接收 parse_basic() 传入的 YoukuItem
        source = response.body.decode("utf-8")  # 将源码转为json结构
        json = loads(source[(source.find('(')+1):source.rfind(')')])
        item['cmt_num'] = json['data']['sourceCommentSize']
        comments = list(json['data']['comment'])
        cmt_list = []   # 评论Item列表
        for cmt in comments:
            comment = CommentItem()
            comment['id'] = cmt['id']
            comment['id_user'] = cmt['userId']
            comment['id_parent'] = cmt['parentCommentId']
            comment['at_users'] = cmt['atUsers']
            comment['content'] = cmt['content']
            comment['time'] = cmt['createTime']
            comment['num_up'] = cmt['upCount']
            comment['num_down'] = cmt['downCount']
            comment['num_reply'] = cmt['replyCount']
            cmt_list.append(comment)
        item['comment'] = cmt_list  # 将列表填入 YoukuItem
        yield item  # 返回填写好的 YoukuItem

    # 拼接评论链接
    def get_cmt_url(self, vid):
        cmt_url = self.scheme
        cmt_url += "//p.comments.youku.com"         # host
        cmt_url += "/ycp/comment/pc/commentList"    # path
        cmt_url += "?jsoncallback=n_commentList"    # query
        cmt_url += "&app=" + "100-DDwODVkv"
        cmt_url += "&objectId=" + vid
        cmt_url += "&objectType=" + "1"
        cmt_url += "&listType=" + "0"
        cmt_url += "&currentPage=" + "1"
        cmt_url += "&pageSize=" + "30"
        cmt_url += "&sign=" + "df030fad8c097139f7fd726e85f63339"
        cmt_url += "&time=" + "1526430304"
        return cmt_url



