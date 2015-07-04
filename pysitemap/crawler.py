import urllib
from bs4 import BeautifulSoup
import urlparse
import mechanize
import pickle
import re
try:                    
    import gevent
    from gevent import monkey, pool
    monkey.patch_all()
    gevent_installed = True
except:
    print("Gevent does not installed. Parsing process will be slower.")
    gevent_installed = False


class Crawler:
    def __init__(self, url, outputfile='sitemap.xml', logfile='error.log', oformat='xml'):
        self.url = url
        self.logfile = open(logfile, 'a')
        self.oformat = oformat
        self.outputfile = outputfile

        # create lists for the urls in que and visited urls
        self.urls = set([url])
        self.visited = set([url])
        self.exts = ['htm', 'php']
        self.allowed_regex = '\.((?!htm)(?!php)\w+)$'

    def set_exts(self, exts):
        self.exts = exts

    def allow_regex(self, regex=None):
        if not regex is None:
            self.allowed_regex = regex
        else:
            allowed_regex = ''
            for ext in self.exts:
                allowed_regex += '(!{})'.format(ext)
            self.allowed_regex = '\.({}\w+)$'.format(allowed_regex)

    def crawl(self, echo=False, pool_size=1):
        self.echo = echo
        self.regex = re.compile(self.allowed_regex)
        if gevent_installed and pool_size > 1:
            self.pool = pool.Pool(pool_size)
            self.pool.spawn(self.parse_gevent)
            self.pool.join()
        else:
            while len(self.urls) > 0:
                self.parse()
        if self.oformat == 'xml':
            self.write_xml()

    def parse_gevent(self):
        self.parse()
        while len(self.urls) > 0 and not self.pool.full():
            self.pool.spawn(self.parse_gevent)

    def parse(self):
        if self.echo:
            if not gevent_installed:
                print('{} pages parsed :: {} pages in the queue'.format(len(self.visited), len(self.urls)))
            else:
                print('{} pages parsed :: {} parsing processes  :: {} pages in the queue'.format(len(self.visited), len(self.pool), len(self.urls)))

        # Set the startingpoint for the spider and initialize 
        # the a mechanize browser object

        if not self.urls:
            return
        else:
            url = self.urls.pop()
            br = mechanize.Browser()
            try:
                response = br.open(url)
                if response.code >= 400:
                    self.errlog("Error {} at url {}".format(response.code, url))
                    return
                           
                for link in br.links():
                    newurl =  urlparse.urljoin(link.base_url, link.url)
                    #print newurl
                    if self.is_valid(newurl):
                        self.visited.update([newurl])
                        self.urls.update([newurl])
            except Exception, e:
                self.errlog(e.message)

            br.close()
            del(br)



    def is_valid(self, url):
        valid = False
        if url in self.visited:
            return False
        if not self.url in url:
            return False
        if re.search(self.regex, url):
            return False
        return True

    def errlog(self, msg):
        self.logfile.write(msg)
        self.logfile.write('\n')

    def write_xml(self):
        of = open(self.outputfile, 'w')
        of.write('<?xml version="1.0" encoding="utf-8"?>\n')
        of.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">\n')
        url_str = '<url><loc>{}</loc></url>\n'
        while self.visited:
            of.write(url_str.format(self.visited.pop()))

        of.write('</urlset>')
        of.close()




