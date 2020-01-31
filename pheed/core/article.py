"""Article definition and related utilities

"""

import typing

from pheed.core.author import Author


class Article:
    def __init__(self, title: str, authors: typing.Tuple[Author, ...], url: str, summary: str = None):
        self.title = title
        self.authors = authors
        self.url = url
        self.summary = summary
