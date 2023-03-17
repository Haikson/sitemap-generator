import asyncio
import signal
from pysitemap.base_crawler import Crawler
import logging
logger = logging.getLogger(__name__)


def crawler(
    root_url, out_file, out_format='xml', maxtasks=100,
    exclude_urls=None, http_request_options=None,
    parser=None
):
    """
    run crowler
    :param root_url: Site root url
    :param out_file: path to the out file
    :param out_format: format of out file [xml, txt]
    :param maxtasks: max count of tasks
    :return:
    """
    loop = asyncio.get_event_loop()
    c = Crawler(
        root_url, out_file=out_file, out_format=out_format, maxtasks=maxtasks, http_request_options=http_request_options
    )
    
    if parser is not None:
        c.set_parser(parser_class=parser)

    if exclude_urls:
        c.set_exclude_url(urls_list=exclude_urls)

    loop.run_until_complete(c.run())

    try:
        loop.add_signal_handler(signal.SIGINT, loop.stop)
    except RuntimeError:
        pass
    logger.info('todo_queue:', len(c.todo_queue))
    logger.info('busy:', len(c.busy))
    logger.info('done:', len(c.done), '; ok:', sum(c.done.values()))
    logger.info('tasks:', len(c.tasks))