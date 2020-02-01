"""Tests for APS source"""
import functools
import pathlib

import apsjournals
import mock
import pytest
from apsjournals.api import Author as APSAuthor, Article as APSArticle
from apsjournals.web.constants import EndPoint

from pheed.core.article import Article
from pheed.core.author import Author
from pheed.sources import aps

STATIC_DIR = pathlib.Path(__file__).parent / 'static' / 'aps'


def get_params_from_url(url: str, ep: EndPoint) -> tuple:
    m = ep.as_re().match(url)
    if m is not None:
        return m.groups()
    raise ValueError('Unable to match url against known endpoints: {}'.format(url))


def get_aps_static(url: str, ep: EndPoint):
    params = get_params_from_url(url, ep)
    if len(params) == 2:  # missing issue
        params = params + (None,)
    journal, volume, issue = params
    file_name = str(volume) + ('' if issue is None else '-' + str(issue)) + '.htm'
    p = STATIC_DIR / journal / file_name
    with open(p.as_posix()) as fid:
        return fid.read()


def issue_get_static(**kwargs):
    return get_aps_static(url=EndPoint.Issue.format(**kwargs), ep=EndPoint.Issue)


class TestAPSSource:
    @pytest.fixture(scope='class', autouse=True)
    def source(self):
        return aps.APSSource(apsjournals.PRL.name)

    def test_recent(self, source):
        with mock.patch('apsjournals.web.scrapers.get_aps', side_effect=functools.partial(get_aps_static, ep=EndPoint.Volume)):
            with mock.patch('apsjournals.web.scrapers.IssueScraper.get', side_effect=issue_get_static):
                articles = source.recent()
        assert isinstance(articles, list)
        assert len(articles) > 0
        assert isinstance(articles[0], Article)


class TestAPSCoercions:
    @pytest.fixture(scope='class', autouse=True)
    def author(self):
        return APSAuthor('last, first')

    @pytest.fixture(scope='class', autouse=True)
    def article(self, author):
        return APSArticle('issue', 'name', [author], 'url', 'pdf_url', 'teaser')

    def test_aps_author_to_pheed_author(self, author):
        coerced = aps.aps_author_to_pheed_author(author)
        assert coerced == Author('first', 'last')

    def test_aps_article_to_pheed_article(self, author, article):
        coerced = aps.aps_article_to_pheed_article(article)
        assert coerced == Article('name', (aps.aps_author_to_pheed_author(author),), 'url', 'teaser')
