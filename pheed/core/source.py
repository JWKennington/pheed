"""Core definition for an article source and related utilities
"""

import abc
import typing

from pheed.core.article import Article
from pheed.core.common import PheedException

Results = typing.List[Article]


class SourceException(PheedException):
    """Exception related to behavior of sources"""


class Source(abc.ABC):
    """Source interface definition outlines common methods that any Source must support.
    Note, this class is an abstract base class and therefore is not intended to be instantiated directly.
    """

    def __init__(self, name: str):
        """Create a source

        Args:
            name:
                str, the name of the source

        Notes:
              BaseClass: This __init__ is not intended to be called directly
        """
        self.name = name

    def search(self, **kwargs) -> Results:
        raise NotImplementedError

    def recent(self, **kwargs) -> Results:
        raise NotImplementedError
