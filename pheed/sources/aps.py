"""Wrappers for the APS source

References:
    [1] APS Journals home page https://journals.aps.org/about
    [2] APS terms and conditions https://journals.aps.org/info/terms.html
"""

import apsjournals
from apsjournals.api import Article as APSArticle, Author as APSAuthor

from pheed.core import source
from pheed.core.article import Article
from pheed.core.author import Author
from pheed.core.source import Results

_JOURNALS = [
    # These journals below define the known APS journals
    apsjournals.PRA,
    apsjournals.PRAB,
    apsjournals.PRApplied,
    apsjournals.PRB,
    apsjournals.PRC,
    apsjournals.PRD,
    apsjournals.PRE,
    apsjournals.PRFluids,
    apsjournals.PRL,
    apsjournals.PRM,
    apsjournals.PRMaterials,
    apsjournals.PRPER,
    apsjournals.PRX
]
_JOURNAL_LOOKUP = {j.name: j for j in _JOURNALS}


class APSSource(source.Source):
    """An APS source is a wrapper around the APSJournals library "Journal" concept
    """

    def __init__(self, name: str):
        """Create an APS Source

        Args:
            name:
                str, must be a known APS publication
        """
        # Check that name is a known APS Publication
        if name not in _JOURNAL_LOOKUP:
            raise source.SourceException(
                'Unknown APS Journal: {!r}. Options are {}'.format(name, ', '.join(_JOURNAL_LOOKUP.keys())))

        # Call Base Source Constructor
        super().__init__(name)

        # APS - specific source attributes
        self.journal = _JOURNAL_LOOKUP[name]

    def search(self, **kwargs) -> Results:
        raise source.SourceException('Search functionality is not available yet for APS Journals')

    def recent(self) -> Results:
        """Get recent articles by checking the most recent issue of the given journal

        Returns:
            List[Article], the recent articles from this APS Journal
        """
        volume = self.journal.volume()
        issue = volume.issue(volume.issues[-1])
        return [aps_article_to_pheed_article(a) for a in issue.articles]


def aps_author_to_pheed_author(author: APSAuthor) -> Author:
    """Convert an APSJournals Author to a Pheed Author

    Args:
        author:
            APSJournals Author

    Returns:
        Pheed Author
    """
    return Author(first_name=author.first_name, last_name=author.last_name)


def aps_article_to_pheed_article(article: APSArticle) -> Article:
    """Convert an APSJournals Article to a Pheed Article

    Args:
        article:
            APSJournals Article

    Returns:
        Pheed Article
    """
    return Article(title=article.name,
                   authors=tuple([aps_author_to_pheed_author(a) for a in article.authors]),
                   url=article.url,
                   summary=article.teaser)
