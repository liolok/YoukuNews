# -*- coding: utf-8 -*-

# Scrapy settings for YoukuNews project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'YoukuNews'

SPIDER_MODULES = ['YoukuNews.spiders']
NEWSPIDER_MODULE = 'YoukuNews.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'YoukuNews (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'YoukuNews.middlewares.YoukunewsSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'YoukuNews.middlewares.YoukunewsDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'YoukuNews.pipelines.YoukunewsPipeline': 300,
    'YoukuNews.pipelines.ThumbPipeline': 1,
    'YoukuNews.pipelines.FilesPipeline': 2,
}

# Configure media pipelines, 媒体文件下载配置
# https://doc.scrapy.org/en/latest/topics/media-pipeline.html
# Configure files pipelines, 视频文件下载配置
FILES_STORE = './Downloads/'  # 统一下载文件夹, 在pipeline中进一步区分
FILES_RESULT_FIELD = 'file_paths'  # 自定义下载结果Field
# Configure images pipelines, 缩略图下载配置
IMAGES_STORE = './Downloads/'  # 统一下载文件夹, 在pipeline中进一步区分
IMAGES_URLS_FIELD = 'thumb_url'  # 自定义链接Field
IMAGES_MIN_HEIGHT = 110  # 最小高度
IMAGES_MIN_WIDTH = 110  # 最小宽度

# Configure MongoDB, 数据库配置
# 安装MongoDB: https://docs.mongodb.com/manual/installation/
# 安装pymongo: https://api.mongodb.com/python/current/installation.html
# URI格式文档: https://docs.mongodb.com/manual/reference/connection-string/
MONGO_URI = "127.0.0.1:27017"  # URI, 用于连接应用与MongoDB实例
MONGO_DB = "YoukuNews"  # 数据库名称

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
