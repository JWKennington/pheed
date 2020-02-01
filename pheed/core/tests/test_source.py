"""Tests for Source interface"""

from pheed.core import source


class DummySource(source.Source):
    pass


class TestSource:
    def test_create_source(self):
        s = DummySource('name')
