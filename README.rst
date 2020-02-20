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

    if __name__ == '__main__':
        if '--iocp' in sys.argv:
            from asyncio import events, windows_events
            sys.argv.remove('--iocp')
            logging.info('using iocp')
            el = windows_events.ProactorEventLoop()
            events.set_event_loop(el)

        # root_url = sys.argv[1]
        root_url = 'https://www.haikson.com'
        crawler(root_url, out_file='sitemap.xml')

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

v. 0.9.2
''''''''

-  todo queue and done list backends
-  created very slowest sqlite backend for todo queue and done lists (1000 url writing for 3 minutes)
-  tests for sqlite_todo backend

v. 0.9.1
''''''''

-  extended readme
-  docstrings and code commentaries

v. 0.9.0
''''''''

-  since this version package supports only python version >=3.7
-  all functions recreated but api saved. If You use this package, then
   just update it, install requirements and run process
-  all requests works asynchronously

