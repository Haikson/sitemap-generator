# -*- coding: utf-8 -*-
import __future__
import sys
if sys.version_info.major == 2:
    import urlparse
else:
    from urllib import parse as urlparse
import requests
from lxml import html
import re
import time
try:
    import sys
    if 'threading' in sys.modules:
        del sys.modules['threading']
        print('threading module loaded before patching!')
        print('threading module deleted from sys.modules!\n')
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
        self.errors = {'404': []}

    def set_exts(self, exts):
        self.exts = exts

    def allow_regex(self, regex=None):
        if regex is not None:
            self.allowed_regex = regex
        else:
            allowed_regex = ''
            for ext in self.exts:
                allowed_regex += '(!{})'.format(ext)
            self.allowed_regex = '\.({}\w+)$'.format(allowed_regex)

    def crawl(self, echo=False, pool_size=1):
        # sys.stdout.write('echo attribute deprecated and will be removed in future')
        self.echo = echo
        self.regex = re.compile(self.allowed_regex)

        print('Parsing pages')
        if gevent_installed and pool_size >= 1:
            self.pool = pool.Pool(pool_size)
            self.pool.spawn(self.parse_gevent)
            self.pool.join()
        else:
            self.pool = [None,] # fixing n_poll exception in self.parse with poolsize > 1 and gevent_installed == False
            while len(self.urls) > 0:
                self.parse()
        if self.oformat == 'xml':
            self.write_xml()
        elif self.oformat == 'txt':
            self.write_txt()
        with open('errors.txt', 'w') as err_file:
            for key, val in self.errors.items():
                err_file.write(u'\n\nError {}\n\n'.format(key))
                err_file.write(u'\n'.join(set(val)))

    def parse_gevent(self):
        self.parse()
        while len(self.urls) > 0 and not self.pool.full():
            self.pool.spawn(self.parse_gevent)

    def parse(self):
        if self.echo:
            n_visited, n_urls, n_pool = len(self.visited), len(self.urls), len(self.pool)
            status = (
                '{} pages parsed :: {} pages in the queue'.format(n_visited, n_urls),
                '{} pages parsed :: {} parsing processes  :: {} pages in the queue'.format(n_visited, n_pool, n_urls)
            )
            print(status[int(gevent_installed)])

        if not self.urls:
            return
        else:
            url = self.urls.pop()
            try:
                response = requests.get(url)
                # if status code is not 404, then add url in seld.errors dictionary
                if response.status_code != 200:
                    if self.errors.get(str(response.status_code), False):
                        self.errors[str(response.status_code)].extend([url])
                    else:
                        self.errors.update({str(response.status_code): [url]})
                    self.errlog("Error {} at url {}".format(response.status_code, url))
                    return

                try:
                    tree = html.fromstring(response.text)
                except ValueError as e:
                    self.errlog(repr(e))
                    tree = html.fromstring(response.content)
                for link_tag in tree.findall('.//a'):
                    link = link_tag.attrib.get('href', '')
                    newurl = urlparse.urljoin(self.url, link)
                    # print(newurl)
                    if self.is_valid(newurl):
                        self.visited.update([newurl])
                        self.urls.update([newurl])
            except Exception as e:
                self.errlog(repr(e))

    def is_valid(self, url):
        oldurl = url
        if '#' in url:
            url = url[:url.find('#')]
        if url in self.visited or oldurl in self.visited:
            return False
        if self.url not in url:
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

    def write_txt(self):
        of = open(self.outputfile, 'w')
        url_str = u'{}\n'
        while self.visited:
            of.write(url_str.format(self.visited.pop()))

        of.close()

    def show_progress(self, count, total, status=''):
        bar_len = 60
        filled_len = int(round(bar_len * count / float(total)))

        percents = round(100.0 * count / float(total), 1)
        bar = '=' * filled_len + '-' * (bar_len - filled_len)
        sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
        sys.stdout.flush()  # As suggested by Rom Ruben (see: http://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console/27871113#comment50529068_27871113)
        time.sleep(0.5)
