# -*- coding: utf-8 -*-

from scrapy import Spider, Request
from YoukuNews.items import VideoItem, CommentItem
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
        video_list = []  # 创建视频信息列表
        for v in response.css('.v'):  # 遍历目录页面
            video = VideoItem()  # 循环实例化 VideoItem, 并解析基本信息填入
            link = v.css('.v-link').xpath('./a/@href').re('(//v.youku.com/v_show/id_([A-Za-z0-9]+))')
            video['vid'] = link[1]                   # 链接id字段
            video['url'] = self.scheme + link[0]     # 补全协议类型
            video['title'] = v.css('.v-link').xpath('./a/@title').extract_first()
            video['thumb_url'] = self.scheme + v.css('.v-thumb').xpath('./img/@src').re_first('//.+')
            video['time'] = v.css('.v-time::text').extract_first()
            video['statplay'] = v.css('.ico-statplay+span::text').extract_first()        # 播放图标后面的文本
            video['statcomment'] = v.css('.ico-statcomment+span::text').extract_first()  # 评论图标后面的文本
            video_list.append(video)  # 追加视频信息列表
        for video in video_list:  # 回调 parse_detail() 对列表中的每个 VideoItem 的视频页面进行解析
            yield Request(url=video['url'], meta={'item': video}, callback=self.parse_detail)

    # 预编译正则表达式, 用于解析视频页面详细信息
    re_subtitle = compile(r'subtitle\\\" title=\\\"(.+?)\\\">')                         # 副标题
    re_category = compile(r'irCategory\\\" content=\\\"(.+?)\\\"')                      # 分类
    re_channame = compile(r'module_basic_sub.+?alt.+?\\n\s+(.+?)\\')                    # 频道名称
    re_chanlink = compile(r'module_basic_sub.+?(//i\.youku\.com/i/(?:[A-Za-z0-9]+))')   # 频道链接

    # 从视频页面解析详细信息
    def parse_detail(self, response):
        video = response.meta['item']  # 接收 parse_basic() 传入的 VideoItem
        source = response.body.decode("utf-8")  # 对源码进行正则匹配
        video['subtitle'] = self.re_subtitle.search(source).group(1)
        video['category'] = self.re_category.search(source).group(1)
        video['channel_name'] = self.re_channame.search(source).group(1)
        video['channel_link'] = self.scheme + self.re_chanlink.search(source).group(1)
        # 回调 parse_comment() 对当前 VideoItem 的评论源码进行解析
        video['comment_list'] = []
        yield Request(url=self.get_cmt_url(video['vid'], "1"),
                      meta={'item': video},
                      callback=self.parse_comment)

    # 从评论源码解析评论信息
    def parse_comment(self, response):
        video = response.meta['item']  # 接收 parse_detail() 传入的 VideoItem
        source = response.body.decode("utf-8")  # 将源码转为json结构
        json = loads(source[(source.find('(') + 1):source.rfind(')')])
        page_current = json['data']['currentPage']  # 当前页码
        page_total = json['data']['totalPage']      # 页码总数
        if page_current is 1:   # 评论数目和热评id在评论首页获取一次即可
            video['comment_num'] = json['data']['sourceCommentSize']  # 源码评论数目
            video['comment_hot'] = []  # 热评id列表
            for hot in list(json['data']['hot']):
                video['comment_hot'].append(hot['id'])
        comments = list(json['data']['comment'])
        for c in comments:
            cmt = CommentItem()
            cmt['id'] = c['id']
            cmt['id_user'] = c['userId']
            cmt['id_parent'] = c['parentCommentId']
            cmt['at_users'] = c['atUsers']
            cmt['content'] = c['content']
            cmt['time'] = c['createTime']
            cmt['num_up'] = c['upCount']
            cmt['num_down'] = c['downCount']
            cmt['num_reply'] = c['replyCount']
            video['comment_list'].append(cmt)
        if page_current < page_total:
            yield Request(url=self.get_cmt_url(video['vid'], str(page_current + 1)),
                          meta={'item': video},
                          callback=self.parse_comment)
        else:
            yield video  # 返回填写好的 VideoItem

    # 拼接评论链接
    def get_cmt_url(self, vid, page):
        cmt_url = self.scheme
        cmt_url += "//p.comments.youku.com"         # host
        cmt_url += "/ycp/comment/pc/commentList"    # path
        cmt_url += "?jsoncallback=n_commentList"    # query
        cmt_url += "&app=" + "100-DDwODVkv"
        cmt_url += "&objectId=" + vid
        cmt_url += "&objectType=" + "1"
        cmt_url += "&listType=" + "0"
        cmt_url += "&currentPage=" + page
        cmt_url += "&pageSize=" + "30"
        cmt_url += "&sign=" + "df030fad8c097139f7fd726e85f63339"
        cmt_url += "&time=" + "1526430304"
        return cmt_url
