pysitemap
=========

Sitemap generator

installing
----------

::

    pip install sitemap-generator

requirements
------------

::

    asyncio
    aiofile
    aiohttp

example
-------

::

    import sys
    import logging
    from pysitemap import crawler
    from pysitemap.parsers.lxml_parser import Parser

    if __name__ == '__main__':
        if '--iocp' in sys.argv:
            from asyncio import events, windows_events
            sys.argv.remove('--iocp')
            logging.info('using iocp')
            el = windows_events.ProactorEventLoop()
            events.set_event_loop(el)

        # root_url = sys.argv[1]
        root_url = 'https://www.haikson.com'
        crawler(
            root_url, out_file='debug/sitemap.xml', exclude_urls=[".pdf", ".jpg", ".zip"],
            http_request_options={"ssl": False}, parser=Parser
        )

TODO
-----

-  big sites with count of pages more then 100K will use more then 100MB
   memory. Move queue and done lists into database. Write Queue and Done
   backend classes based on
-  Lists
-  SQLite database
-  Redis
-  Write api for extending by user backends

changelog
---------

