import pysitemap

"""
Example script
"""

if __name__=='__main__':
<<<<<<< HEAD
    url = 'http://www.ltsvet.ru/' # url from to crawl
    logfile = 'errlog.log' # path to logfile
    oformat = 'xml' # output format
    outputfile = '/srv/www/site/sitemap.xml' # path to output file
    crawl = pysitemap.Crawler(url=url, logfile=logfile, oformat=oformat, outputfile=outputfile)
    crawl.crawl()
=======
    url = 'http://www.example.ru/' # url from to crawl
    logfile = 'errlog.log' # path to logfile
    oformat = 'xml' # output format
    crawl = pysitemap.Crawler(url=url, logfile=logfile, oformat=oformat)
    print datetime.datetime.now()
    crawl.crawl()
    print datetime.datetime.now()
>>>>>>> origin/master
