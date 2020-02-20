import logging
import asyncio
import re
import urllib.parse
from pysitemap.format_processors.xml import XMLWriter
from pysitemap.format_processors.text import TextWriter
import aiohttp


class Crawler:

    format_processors = {
        'xml': XMLWriter,
        'txt': TextWriter
    }

    def __init__(self, rooturl, out_file, out_format='xml', maxtasks=100,
                 todo_queue_backend=set, done_backend=dict):
        """
        Crawler constructor
        :param rooturl: root url of site
        :type rooturl: str
        :param out_file: file to save sitemap result
        :type out_file: str
        :param out_format: sitemap type [xml | txt]. Default xml
        :type out_format: str
        :param maxtasks: maximum count of tasks. Default 100
        :type maxtasks: int
        """
        self.rooturl = rooturl
        self.todo_queue = todo_queue_backend()
        self.busy = set()
        self.done = done_backend()
        self.tasks = set()
        self.sem = asyncio.Semaphore(maxtasks)

        # connector stores cookies between requests and uses connection pool
        self.session = aiohttp.ClientSession()
        self.writer = self.format_processors.get(out_format)(out_file)

    async def run(self):
        """
        Main function to start parsing site
        :return:
        """
        t = asyncio.ensure_future(self.addurls([(self.rooturl, '')]))
        await asyncio.sleep(1)
        while self.busy:
            await asyncio.sleep(1)

        await t
        await self.session.close()
        await self.writer.write([key for key, value in self.done.items() if value])

    async def addurls(self, urls):
        """
        Add urls in queue and run process to parse
        :param urls:
        :return:
        """
        for url, parenturl in urls:
            url = urllib.parse.urljoin(parenturl, url)
            url, frag = urllib.parse.urldefrag(url)
            if (url.startswith(self.rooturl) and
                    url not in self.busy and
                    url not in self.done and
                    url not in self.todo_queue):
                self.todo_queue.add(url)
                # Acquire semaphore
                await self.sem.acquire()
                # Create async task
                task = asyncio.ensure_future(self.process(url))
                # Add collback into task to release semaphore
                task.add_done_callback(lambda t: self.sem.release())
                # Callback to remove task from tasks
                task.add_done_callback(self.tasks.remove)
                # Add task into tasks
                self.tasks.add(task)

    async def process(self, url):
        """
        Process single url
        :param url:
        :return:
        """
        print('processing:', url)

        # remove url from basic queue and add it into busy list
        self.todo_queue.remove(url)
        self.busy.add(url)

        try:
            resp = await self.session.get(url)  # await response
        except Exception as exc:
            # on any exception mark url as BAD
            print('...', url, 'has error', repr(str(exc)))
            self.done[url] = False
        else:
            # only url with status == 200 and content type == 'text/html' parsed
            if (resp.status == 200 and
                    ('text/html' in resp.headers.get('content-type'))):
                data = (await resp.read()).decode('utf-8', 'replace')
                urls = re.findall(r'(?i)href=["\']?([^\s"\'<>]+)', data)
                asyncio.Task(self.addurls([(u, url) for u in urls]))

            # even if we have no exception, we can mark url as good
            resp.close()
            self.done[url] = True

        self.busy.remove(url)
        logging.info(len(self.done), 'completed tasks,', len(self.tasks),
              'still pending, todo_queue', len(self.todo_queue))


