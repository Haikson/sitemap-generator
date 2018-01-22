import pysitemap

"""
Example script
Uses gevent to implement multiprocessing if Gevent installed
To install gevent:
    $ pip install gevent
"""

if __name__ == '__main__':
    url = 'http://www.lumpro.ru/'  # url from to crawl
    logfile = 'errlog.log'  # path to logfile
    oformat = 'xml'  # output format
    outputfile = 'sitemap.xml'  # path to output file
    crawl = pysitemap.Crawler(url=url, logfile=logfile, oformat=oformat, outputfile=outputfile)
    crawl.crawl(pool_size=20, echo=True)
