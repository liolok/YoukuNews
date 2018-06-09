rd /q /s "D:/YoukuNews/Downloads"
del crawl.log
scrapy crawl --logfile=crawl.log youku -a category=jrrm -a page_num=1
pause
