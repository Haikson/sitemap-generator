import asyncio
import signal
from pysitemap.base_crawler import Crawler


def crawler(root_url, out_file, out_format='xml', maxtasks=100):
    """
    run crowler
    :param root_url: Site root url
    :param out_file: path to the out file
    :param out_format: format of out file [xml, txt]
    :param maxtasks: max count of tasks
    :return:
    """
    loop = asyncio.get_event_loop()

    c = Crawler(root_url, out_file=out_file, out_format=out_format, maxtasks=maxtasks)
    loop.run_until_complete(c.run())

    try:
        loop.add_signal_handler(signal.SIGINT, loop.stop)
    except RuntimeError:
        pass
    print('todo_queue:', len(c.todo_queue))
    print('busy:', len(c.busy))
    print('done:', len(c.done), '; ok:', sum(c.done.values()))
    print('tasks:', len(c.tasks))