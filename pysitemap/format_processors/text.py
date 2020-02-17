import asyncio
from aiofile import AIOFile, Reader, Writer
import logging


class TextWriter():
    def __init__(self, filename: str):
        self.filename = filename


    async def write(self, urls):
        async with AIOFile(self.filename, 'w') as aiodf:
            writer = Writer(aiodf)

            for url in urls:
                await writer("{}\n".format(url))
            await aiodf.fsync()

