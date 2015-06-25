import pysitemap
import datetime

"""
Example script
"""

if __name__=='__main__':
    url = 'http://www.example.ru/' # url from to crawl
    logfile = 'errlog.log' # path to logfile
    oformat = 'xml' # output format
    crawl = pysitemap.Crawler(url=url, logfile=logfile, oformat=oformat)
    print datetime.datetime.now()
    crawl.crawl()
    print datetime.datetime.now()
