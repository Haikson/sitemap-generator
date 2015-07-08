import urllib
from bs4 import BeautifulSoup
import urlparse
import mechanize
import pickle
import re
try:
    import sys
    import gevent
    from gevent import monkey, pool, queue
    monkey.patch_all()
    if 'threading' in sys.modules:
        del sys.modules['threading']
        print('threading module loaded before patching!\n')
        print('threading module deleted from sys.modules!\n')
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
        self.visited = set([])
        self.excepted = set([])
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
            self.queue = gevent.queue.Queue()
            self.queue.put(self.url)
            self.pool.spawn(self.parse_gevent)
            while not self.queue.empty() and not self.pool.free_count() == pool_size:
                gevent.sleep(0.1)
                while len(self.urls) > 0:
                    self.queue.put(self.urls.pop())
                for x in xrange(0, min(self.queue.qsize(), self.pool.free_count())):
                    self.pool.spawn(self.parse_gevent)
            self.pool.join()
        else:
            while len(self.urls) > 0:
                self.parse()
        if self.oformat == 'xml':
            self.write_xml()
        self.errlog()

    def parse_gevent(self):
        url = self.queue.get(timeout=0)
        try:
            br = mechanize.Browser()
            response = br.open(url)
            if response.code >= 400:
                self.excepted.update([(url, "Error {} at url {}".format(response.code, url))])
                return
                       
            for link in br.links():
                newurl =  urlparse.urljoin(link.base_url, link.url)
                if self.is_valid(newurl):
                    self.visited.update([newurl])
                    self.urls.update([newurl])
        except Exception, e:
            self.excepted.update([(url, e.message)])
            return
        except gevent.queue.Empty:
            br.close()
            if self.echo:
                print('{} pages parsed :: {} parsing processes  :: {} pages in the queue'.format(len(self.visited), len(self.pool), self.queue.qsize()))
            return

        br.close()
        if self.echo:
            print('{} pages parsed :: {} parsing processes  :: {} pages in the queue'.format(len(self.visited), len(self.pool), self.queue.qsize()))


    def parse(self):
        if self.echo:
            print('{} pages parsed :: {} pages in the queue'.format(len(self.visited), len(self.urls)))

        # Set the startingpoint for the spider and initialize 
        # the a mechanize browser object
        url = self.urls.pop()
        br = mechanize.Browser()
        try:
            response = br.open(url)
            if response.code >= 400:
                self.excepted.update([(url, "Error {} at url {}".format(response.code, url))])
                return
                       
            for link in br.links():
                newurl =  urlparse.urljoin(link.base_url, link.url)
                #print newurl
                if self.is_valid(newurl):
                    self.urls.update([newurl])

            self.visited.update([url])
        except Exception, e:
            self.excepted.update([(url, e.message)])

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

    def errlog(self):
        while len(self.excepted) > 0:
            ex = self.excepted.pop()
            self.logfile.write('{}\n'.format('\t'.join(ex)))
        self.logfile.close()

    def write_xml(self):
        of = open(self.outputfile, 'w')
        of.write('<?xml version="1.0" encoding="utf-8"?>\n')
        of.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">\n')
        url_str = '<url><loc>{}</loc></url>\n'
        while self.visited:
            of.write(url_str.format(self.visited.pop()))

        of.write('</urlset>')
        of.close()
