from PreTeX.line_number_map import *
from PreTeX.helper import load
import pytest

class TestLineNumberMap:

    def test_addPair_getEncoded(self):
        clearData()
        addPair(1,1)
        addPair(2,5)

        result = getEncoded()

        expected = "\n\n%PreTex data. Ignore following line.\n"+\
                   "%[1:1,2:5]"

        assert result == expected

    def test_getDecoded(self, monkeypatch):
        def monkeyloader(path):
            return "foo\nbar\n%[1:1,2:5,3:7]"

        monkeypatch.setattr(helper, 'load', monkeyloader)

        result = getDecoded("foopath")

        expected = ["1:1","2:5","3:7"]

        assert result == expected

    def test_getDecoded_can_fail(self, monkeypatch):
        def monkeyloader(path):
            return "bad format :("

        monkeypatch.setattr(helper, 'load', monkeyloader)

        result = getDecoded("bazpath")

        expected = "not found"

        assert result == expected

    def test_getLineNumber(self, monkeypatch):
        def monkeyloader(path):
            return "foo\nbar\n%[1:1,2:5,3:7]"

        monkeypatch.setattr(helper, 'load', monkeyloader)

        result = getLineNumber(6, "barpath")

        expected = '2'

        assert result == expected

    def test_getLineNumber_can_fail(self, monkeypatch):
        def monkeyloader(path):
            return "bad format :("

        monkeypatch.setattr(helper, 'load', monkeyloader)

        result = getLineNumber(6, "barkrakk")

        expected = '6'

        assert result == expected
