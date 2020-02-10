from pysitemap import Crawler
import asyncio
"""
Example script
Uses gevent to implement multiprocessing if Gevent installed
To install gevent:
    $ pip install gevent
"""

if __name__ == '__main__':
    url = 'http://www.stroivopros.ru/'  # url from to crawl
    logfile = 'errlog.log'  # path to logfile
    oformat = 'xml'  # output format
    outputfile = 'sitemap.xml'  # path to output file
    loop = asyncio.get_event_loop()
    crawler = Crawler(url=url, logfile=logfile, oformat=oformat, outputfile=outputfile)
    future = asyncio.ensure_future(crawler.crawl(echo=True))
    loop.run_until_complete(future)

