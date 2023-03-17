import re
from pysitemap.parsers.base import BaseParser


class Parser(BaseParser):

    @classmethod
    def parse(cls, html_string):
        return re.findall(r'(?i)href\s*?=\s*?[\"\']?([^\s\"\'<>]+)[\"\']', html_string)
