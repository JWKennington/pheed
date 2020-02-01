"""Article definition and related utilities

"""

import typing

from pheed.core.author import Author


class Article:
    """An article is a published paper with one or more authors. Each article has a URL pointing to the online
    location where meta data is available (not necessarily the pdf location). Additionally, the Article
    may contain summary information, such as an abstract or teaser.
    """

    def __init__(self, title: str, authors: typing.Tuple[Author, ...], url: str, summary: str = None):
        """Create a Pheed Article

        Args:
            title:
                str, the title of the article
            authors:
                Tuple[Author], a tuple of Pheed Author instances
            url:
                str, the URL of the article (not the pdf)
            summary:
                str, default None, any summary information if available, such as an abstract or a teaser
        """
        self.title = title
        self.authors = authors
        self.url = url
        self.summary = summary

    def __eq__(self, other):
        return isinstance(other, Article) and self._identity_key_() == other._identity_key_()

    def __hash__(self):
        return hash(self._identity_key_())

    def __repr__(self):
        return 'Article({!r})'.format(self.title)

    def _identity_key_(self):
        return (Article, self.title, self.authors, self.url, self.summary)
