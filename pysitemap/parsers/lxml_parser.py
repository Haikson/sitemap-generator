from lxml import etree, cssselect, html
from pysitemap.parsers.base import BaseParser


class Parser(BaseParser):
    """
    LXML based Parser
    """

    @classmethod
    def parse(cls, html_string):
        dochtml = html.fromstring(html_string)
        select = cssselect.CSSSelector("a")
        return [ el.get('href') for el in select(dochtml) ]

