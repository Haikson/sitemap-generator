import pysitemap

"""
Example script
"""

if __name__=='__main__':
    url = 'http://www.ltsvet.ru/' # url from to crawl
    logfile = 'errlog.log' # path to logfile
    oformat = 'xml' # output format
    outputfile = '/srv/www/site/sitemap.xml' # path to output file
    crawl = pysitemap.Crawler(url=url, logfile=logfile, oformat=oformat, outputfile=outputfile)
    crawl.crawl()