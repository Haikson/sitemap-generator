#!/usr/bin/env python3

import time
import asyncio
from aiohttp import ClientSession
from parsel import Selector
from urllib.parse import urlparse, urlunparse


class Crawler(object):
    def __init__(self, url, sleep_time=.5):

        self.urls = [url]
        scheme, netloc, path, params, query, fragment = urlparse(url)
        if not netloc:
            netloc, path = path, netloc
        url = urlunparse((scheme, netloc, "", params, "", fragment))
        self.base_url = url
        self.sleep_time = float(sleep_time)

    async def fetch(self, url, session):
        async with session.get(url) as response:
            await asyncio.sleep(self.sleep_time)
            return response.content

    async def bound_fetch(self, sem, url, session):
        # Getter function with semaphore.
        async with sem:
            await self.fetch(url, session)

    def norm_link(self, url:str):
        if url.startswith(self.base_url):
            return url
        elif url.startswith('//'):
            return "{scheme}{url}".format(
                scheme=self.base_url[:self.base_url.find(":")],
                url=url
            )
        elif url.startswith("/"):
            return self.base_url + url
        return None

    async def parse(self, content):
        sel = Selector(content)
        links = sel.xpath('//a/@href').getall()
        normalized_links = []
        for link in links:
            link = self.norm_link(link)
            if link:
                normalized_links.append(link)
        self.urls.extend(normalized_links)

    async def run(self):
        tasks = []
        # create instance of Semaphore
        sem = asyncio.Semaphore(20)

        # Create client session that will ensure we dont open new connection
        # per each request.
        async with ClientSession() as session:
            for url in self.urls:
                # pass Semaphore and session to every GET request
                task = asyncio.ensure_future(self.bound_fetch(sem, url, session))
                tasks.append(task)

            responses = asyncio.gather(*tasks)
            await responses

