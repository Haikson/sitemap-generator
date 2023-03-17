from abc import ABC, abstractclassmethod
from typing import List


class BaseParser(ABC):

    @abstractclassmethod
    def parse(cls, html_string) -> List[str]:
        """
        Base parse method
        """
        