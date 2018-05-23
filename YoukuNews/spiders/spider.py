# -*- coding: utf-8 -*-

from scrapy import Spider, Request
from YoukuNews.items import VideoItem, CommentItem
from re import compile
from json import loads

class YoukuSpider(Spider):
    name = 'youku'      # 爬虫唯一识别名
    scheme = "https:"   # URL传送协议类型
    allowed_domains = ['youku.com']  # 爬取域名范围

    # 从以下三个目录页面开始解析(减少到一个, 方便调试)
    def start_requests(self):
        yield Request('http://news.youku.com/index/jrrm', self.parse_basic)  # 今日热门
        # yield Request('http://news.youku.com/index/jkjs', self.parse_basic)  # 监控纪实
        # yield Request('http://news.youku.com/index/jsqy', self.parse_basic)  # 军事前沿

    # 从目录页面解析视频列表及每个视频的基本信息
    def parse_basic(self, response):
        video_list = []  # 创建视频信息列表
        for v in response.css('.v'):  # 遍历目录页面
            video = VideoItem()  # 循环实例化 VideoItem, 并解析基本信息填入
            link = v.css('.v-link').xpath('./a/@href').re('(//v.youku.com/v_show/id_([A-Za-z0-9]+))')
            video['url'] = self.scheme + link[0]  # 补全协议类型
            video['vid'] = link[1]  # 链接id字段即为vid
            video['title'] = v.css('.v-link').xpath('./a/@title').extract_first()
            video['thumb_url'] = self.scheme + v.css('.v-thumb').xpath('./img/@src').re_first('//.+')
            video['time'] = v.css('.v-time::text').extract_first()
            video['stat_play'] = v.css('.ico-statplay+span::text').extract_first()    # 播放图标后面的文本
            video['stat_cmt'] = v.css('.ico-statcomment+span::text').extract_first()  # 评论图标后面的文本
            video_list.append(video)  # 追加视频信息列表
        for video in video_list:  # 回调 parse_detail() 对列表中的每个 VideoItem 的视频页面进行解析
            yield Request(url=video['url'], meta={'item': video}, callback=self.parse_detail)

    # 从视频页面解析详细信息
    def parse_detail(self, response):
        video = response.meta['item']  # 接收 parse_basic() 传入的 VideoItem
        source = response.text  # 对源码进行正则匹配
        video['subtitle'] = self.re_subtitle.search(source).group(1)
        video['category'] = self.re_category.search(source).group(1)
        video['channel_name'] = self.re_channame.search(source).group(1)
        video['channel_link'] = self.scheme + self.re_chanlink.search(source).group(1)
        # 回调 parse_file() 解析当前 VideoItem 的文件下载地址列表
        yield Request(url=self.get_ups_url(video['vid']),
                      meta={'item': video},
                      headers=self.headers,
                      cookies=self.cookies,
                      callback=self.parse_file)

    # 从UPS接口解析文件下载链接列表
    def parse_file(self, response):
        video = response.meta['item']  # 接收 parse_detail() 传入的 VideoItem
        text = response.text  # 将源码中的json字符串转换成dict字典
        src = loads(text[(text.find('(') + 1):text.rfind(')')])
        for stm in src['data']['stream']:
            if stm['stream_type'] == 'mp4sd':  # 选择标清并获取其分段链接列表
                video['file_urls'] = [seg['cdn_url'] for seg in stm['segs']]
        # 回调 parse_comment() 对当前 VideoItem 的评论源码进行解析
        video['comment_list'] = []  # 解析过程中追加评论列表
        yield Request(url=self.get_cmt_url(video['vid'], "1"),
                      meta={'item': video},
                      headers={'Referer': video['url']},
                      callback=self.parse_comment)

    # 从评论源码解析评论信息
    def parse_comment(self, response):
        video = response.meta['item']  # 接收 parse_file() 传入的 VideoItem
        text = response.text  # 将源码中的json字符串转换成dict字典
        src = loads(text[(text.find('(') + 1):text.rfind(')')])
        for c in src['data']['comment']:  # 遍历当前页的评论
            cmt = CommentItem()  # 实例化 CommentItem, 并填入评论信息
            cmt['id'] = c['id']
            cmt['id_user'] = c['userId']
            cmt['id_parent'] = c['parentCommentId']
            cmt['at_users'] = c['atUsers']
            cmt['content'] = c['content']
            cmt['time'] = c['createTime']
            cmt['num_up'] = c['upCount']
            cmt['num_down'] = c['downCount']
            cmt['num_reply'] = c['replyCount']
            video['comment_list'].append(cmt)  # 将新增评论追加至评论列表
        page_cur = src['data']['currentPage']  # 当前页码
        page_sum = src['data']['totalPage']    # 页码总数
        if page_cur is 1:  # 评论数目和热评id在首页获取一次即可
            video['comment_num'] = src['data']['sourceCommentSize']  # 源码包含的评论总数目
            video['comment_hot'] = [hot['id'] for hot in src['data']['hot']]  # 热评id列表
        if page_cur < page_sum:  # 递归回调, 遍历下一页
            yield Request(url=self.get_cmt_url(video['vid'], str(page_cur + 1)),
                          meta={'item': video},
                          callback=self.parse_comment)
        else:  # 已遍历末页, 结束递归
            yield video  # 返回填写好的 VideoItem

    # 预编译正则表达式, 用于解析视频页面详细信息
    re_subtitle = compile(r'subtitle\\\" title=\\\"(.+?)\\\">')                         # 副标题
    re_category = compile(r'irCategory\\\" content=\\\"(.+?)\\\"')                      # 分类
    re_channame = compile(r'module_basic_sub.+?alt.+?\\n\s+(.+?)\\')                    # 频道名称
    re_chanlink = compile(r'module_basic_sub.+?(//i\.youku\.com/i/(?:[A-Za-z0-9]+))')   # 频道链接

    # UPS API URL Request Parameters, UPS接口链接请求参数
    # P_sck 来自 WKH 的优酷账号, 特此鸣谢
    P_sck  = 'W2aaE+5jCOmZENJT9Zk0sItuaySRhQ1CuDcHACLPaSJ84g7C2yHG7LOrHnnLpQ9os+AKG1Dtypkk'
    P_sck += '+mTxhfr7p92xaBUMmz2fuI0OoRAs5agU1nLo/X6HA/gbSkezH6BVX/Dobj9Mv63IsIzqFmcUxA=='
    headers = {'Referer': scheme + '//v.youku.com'}
    cookies = {'P_sck': P_sck}

    # UPS API Query Parameters, UPS接口查询参数
    # 来源: https://github.com/zhangn1985/ykdl/issues/270
    ccode = '0502'
    utid  = 'OMofE8kM4gMCARueFdD7Bexs'
    ckey  = 'DIl58SLFxFNndSV1GFNnMQVYkx1PP5tKe1siZu%2F86PR1u%2FWh1Ptd%2BWOZsHHWxysS'
    ckey += 'fAOhNJpdVWsdVJNsfJ8Sxd8WKVvNfAS8aS8fAOzYARzPyPc3JvtnPHjTdKfESTdnuTW6ZP'
    ckey += 'vk2pNDh4uFzotgdMEFkzQ5wZVXl2Pf1%2FY6hLK0OnCNxBj3%2Bnb0v72gZ6b0td%2BWOZ'
    ckey += 'sHHWxysSo%2F0y9D2K42SaB8Y%2F%2BaD2K42SaB8Y%2F%2BahU%2BWOZsHcrxysooUeND'

    # 拼接UPS_API链接
    def get_ups_url(self, vid):
        ups_url = self.scheme
        ups_url += '//ups.youku.com'    # host
        ups_url += '/ups/get.json'      # path
        ups_url += '?callback=json'     # query&parameters
        ups_url += '&vid=' + vid
        ups_url += '&ccode=' + self.ccode
        ups_url += '&client_ip=' + '192.168.1.1'
        ups_url += '&client_ts=' + '1527072900'
        ups_url += '&utid=' + self.utid
        ups_url += '&ckey=' + self.ckey
        return ups_url

    # 拼接评论链接
    def get_cmt_url(self, vid, page):
        cmt_url = self.scheme
        cmt_url += "//p.comments.youku.com"         # host
        cmt_url += "/ycp/comment/pc/commentList"    # path
        cmt_url += "?jsoncallback=n_commentList"    # query&parameters
        cmt_url += "&app=" + "100-DDwODVkv"
        cmt_url += "&objectId=" + vid
        cmt_url += "&objectType=" + "1"
        cmt_url += "&listType=" + "0"
        cmt_url += "&currentPage=" + page
        cmt_url += "&pageSize=" + "30"
        cmt_url += "&sign=" + "df030fad8c097139f7fd726e85f63339"
        cmt_url += "&time=" + "1526430304"
        return cmt_url
