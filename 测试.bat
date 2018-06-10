rd /q /s "D:/YoukuNews/Downloads"
del crawl.log
scrapy crawl --logfile=crawl.log -L INFO youku -a catelog=jrrm -a pages=2
pause
