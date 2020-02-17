import asyncio
import re
import urllib.parse
from pysitemap.format_processors.xml import XMLWriter
import aiohttp


class Crawler:

    format_processors = {
        'xml': XMLWriter
    }

    def __init__(self, rooturl, out_file, out_format='xml', maxtasks=100):
        self.rooturl = rooturl
        self.todo = set()
        self.busy = set()
        self.done = {}
        self.tasks = set()
        self.sem = asyncio.Semaphore(maxtasks)

        # connector stores cookies between requests and uses connection pool
        self.session = aiohttp.ClientSession()
        self.writer = self.format_processors.get(out_format)(out_file)

    async def run(self):
        t = asyncio.ensure_future(self.addurls([(self.rooturl, '')]))
        await asyncio.sleep(1)
        while self.busy:
            await asyncio.sleep(1)

        await t
        await self.session.close()
        await self.writer.write([key for key, value in self.done.items() if value])

    async def addurls(self, urls):
        for url, parenturl in urls:
            url = urllib.parse.urljoin(parenturl, url)
            url, frag = urllib.parse.urldefrag(url)
            if (url.startswith(self.rooturl) and
                    url not in self.busy and
                    url not in self.done and
                    url not in self.todo):
                self.todo.add(url)
                await self.sem.acquire()
                task = asyncio.ensure_future(self.process(url))
                task.add_done_callback(lambda t: self.sem.release())
                task.add_done_callback(self.tasks.remove)
                self.tasks.add(task)

    async def process(self, url):
        print('processing:', url)

        self.todo.remove(url)
        self.busy.add(url)
        try:
            resp = await self.session.get(url)
        except Exception as exc:
            print('...', url, 'has error', repr(str(exc)))
            self.done[url] = False
        else:
            if (resp.status == 200 and
                    ('text/html' in resp.headers.get('content-type'))):
                data = (await resp.read()).decode('utf-8', 'replace')
                urls = re.findall(r'(?i)href=["\']?([^\s"\'<>]+)', data)
                asyncio.Task(self.addurls([(u, url) for u in urls]))

            resp.close()
            self.done[url] = True

        self.busy.remove(url)
        print(len(self.done), 'completed tasks,', len(self.tasks),
              'still pending, todo', len(self.todo))


