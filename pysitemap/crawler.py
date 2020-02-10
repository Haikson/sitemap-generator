#!/usr/bin/env python3

import time
import asyncio
from aiohttp import ClientSession

class Knocker(object):
    def __init__(self, urls=None, sleep_time=.5):
        self.urls = urls or []
        self.sleep_time = float(sleep_time)

    async def fetch(self, url, session):
        async with session.get(url) as response:
            await asyncio.sleep(self.sleep_time)
            status = response.status
            date = response.headers.get("DATE")
            print("{}:{} with status {}".format(date, response.url, status))
            return url, status

    async def bound_fetch(self, sem, url, session):
        # Getter function with semaphore.
        async with sem:
            await self.fetch(url, session)

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

