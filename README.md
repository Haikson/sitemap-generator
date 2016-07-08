# pysitemap
Sitemap generator

## installing

  pip install sitemap-generator

## Gevent

Sitemap-generator uses [gevent](http://www.gevent.org/) to implement multiprocessing. Install gevent:

  pip install gevent

## example

    import pysitemap


    if __name__ == '__main__':
        url = 'http://www.example.com/'  # url from to crawl
        logfile = 'errlog.log'  # path to logfile
        oformat = 'xml'  # output format
        crawl = pysitemap.Crawler(url=url, logfile=logfile, oformat=oformat)
        crawl.crawl()


## multiprocessing example


    import pysitemap


    if __name__ == '__main__':
        url = 'http://www.example.com/'  # url from to crawl
        logfile = 'errlog.log'  # path to logfile
        oformat = 'xml'  # output format
        crawl = pysitemap.Crawler(url=url, logfile=logfile, oformat=oformat)
        crawl.crawl(pool_size=10)  # 10 parsing processes
