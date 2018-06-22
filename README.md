# 技术文档

## 环境依赖

### 语言: [Pyhton 3](https://docs.python.org/3/)

> 对于 Windows 平台, 建议在安装时勾选"Add Python 3.x to PATH", 或者[设置环境变量](https://docs.python.org/3/using/windows.html#setting-envvars)以通过命令行使用 Python.

### 框架: [Scrapy 1.5](https://doc.scrapy.org/en/1.5/)

> 对于 Windows 平台, 建议使用 [**Anaconda**](https://docs.anaconda.com/anaconda/) (或 [Miniconda](https://conda.io/docs/user-guide/install/index.html)) 的 `conda install -c conda-forge scrapy` 而不是 ~~`pip3 install`~~ 以避免可能出现的依赖问题.

### 其他模块

- `PyMongo`, 用于将视频信息写入MongoDB数据库;
- `Pillow`, 用于处理视频封面图片.

`pip3 install pymongo pillow`


## 数据结构

### 视频信息

> `dict` in Python / `Document` in MongoDB

Key            | Type in Python   | Type in MongoDB     | 含义
-------------- | ---------------- | ------------------- | ------------------------
`url`          | `str`            | `String`            | 页面链接
`vid`          | `str`            | `String`            | 唯一识别码
`time`         | `str`            | `String`            | 时长
`title`        | `str`            | `String`            | 标题
`subtitle`     | `str`            | `String`            | 副标题
`stat_play`    | `str`            | `String`            | 播放量
`stat_cmt`     | `str`            | `String`            | 评论量
`category`     | `str`            | `String`            | 分类
`channel_name` | `str`            | `String`            | 频道名称
`channel_link` | `str`            | `String`            | 频道链接
`comment_num`  | `int`            | `Int32`             | 评论数目
`comment_hot`  | `list` of `int`  | `Array` of `Int64`  | 热评ID列表
`comment_list` | `list` of `dict` | `Array` of `Object` | 所有评论列表(评论信息若干) 
`thumb_url`    | `str`            | `String`            | 缩略图下载链接
`thumb_path`   | `str`            | `String`            | 缩略图本地路径
`file_urls`    | `list` of `str`  | `Array` of `String` | 分段视频文件下载链接列表
`file_paths`   | `list` of `str`  | `Array` of `String` | 分段视频文件本地路径列表

### 评论信息

> `dict` in Python / `Object` in MongoDB

Key         | Type in Python | Type in MongoDB | 含义
----------- | -------------- | --------------- | ----------
`id`        | `int`          | `Int64`         | 唯一识别码
`time`      | `int`          | `Int64`         | 发布时间戳
`user`      | `int`          | `Int32`         | 发布用户ID
`num_up`    | `int`          | `Int32`         | 点赞数
`num_down`  | `int`          | `Int32`         | 点踩数
`num_reply` | `int`          | `Int32`         | 回复数
`content`   | `str`          | `String`        | 评论内容

## 数据流

> 下图取自Scrapy官方文档, 更多详情其中的[Architecture overview(架构概览)](https://doc.scrapy.org/en/1.5/topics/architecture.html)章节.

![Scrapy 系统架构图](https://doc.scrapy.org/en/1.5/_images/scrapy_architecture_02.png)

<center>Scrapy 数据流</center>

> 目前本爬虫只涉及到上图中的`Items`, `Spiders`以及`Item Pipelines`, 其他Scrapy组件几乎并未修改, 均使用默认配置.
