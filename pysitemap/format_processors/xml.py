import asyncio
from aiofile import AIOFile, Reader, Writer
import logging


class XMLWriter():
    def __init__(self, filename: str):
        self.filename = filename


    async def write(self, urls):
        async with AIOFile(self.filename, 'w') as aiodf:
            writer = Writer(aiodf)
            await writer('<?xml version="1.0" encoding="utf-8"?>\n')
            await writer(
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"'
                ' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'
                ' xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">\n')
            await aiodf.fsync()
            for url in urls:
                await writer('<url><loc>{}</loc></url>\n'.format(url))
            await aiodf.fsync()

            await writer('</urlset>')
            await aiodf.fsync()

