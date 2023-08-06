"""
Tests of Filter + Sort Strings in a Python Context
"""
import logging
import unittest

from dada_types.flt import FilterString
from dada_test import BaseTest

FLT_TEST_LOGGER = logging.getLogger()


class FilterStringTests(BaseTest):
    def test_filter_string_gt(self):
        fs = FilterString("foo:>:10", context="py", type="int")
        assert fs.match("11")
        fs = FilterString("foo:gt:10", context="py", type="int")
        assert fs.match(11)
        fs = FilterString("foo:gt:10", context="py", type="int")
        assert not fs.match_fields({"foo": 10})
        assert fs.match_fields({"foo": 11})
        fs = FilterString("foo:gt:9", context="py", type="int")
        assert not fs.match_fields({"bar": 10})

    def test_filter_string_gte(self):
        fs = FilterString("foo:>=:10", context="py", type="int")
        assert fs.match("11")
        fs = FilterString("foo:gte:10", context="py", type="int")
        assert fs.match(11)
        fs = FilterString("foo:gte:10", context="py", type="int")
        assert fs.match_fields({"foo": 10})
        fs = FilterString("foo:gte:10", context="py", type="int")
        assert not fs.match_fields({"bar": 10})

    def test_filter_string_gte_date(self):
        fs = FilterString("foo:>=:2015-01-01", context="py", type="date")
        assert fs.match("2016-01-01")
        fs = FilterString("foo:gte:2014-01-01", context="py", type="date")
        assert fs.match("2014-01-02")

    def test_filter_string_lte(self):
        fs = FilterString("foo:<=:10", context="py", type="int")
        assert fs.match("9")
        fs = FilterString("foo:lte:10", context="py", type="int")
        assert fs.match(9)
        fs = FilterString("foo:lte:10", context="py", type="int")
        assert fs.match_fields({"foo": 10})
        assert not fs.match_fields({"bar": 10})

    def test_filter_string_lt(self):
        fs = FilterString("foo:<:10", context="py", type="int")
        assert fs.match("9")
        fs = FilterString("foo:lt:10", context="py", type="int")
        assert fs.match(9)
        fs = FilterString("foo:lt:10", context="py", type="int")
        assert fs.match_fields({"foo": 9})
        assert not fs.match_fields({"foo": 10})
        assert not fs.match_fields({"bar": 10})

    def test_filter_string_eq(self):
        fs = FilterString("foo:==:10", context="py", type="int")
        assert fs.match("10")
        fs = FilterString("foo:eq:10", context="py", type="int")
        assert fs.match(10)
        fs = FilterString("foo:==:10", context="py", type="int")
        assert fs.match_fields({"foo": 10})

    def test_filter_string_neq(self):
        fs = FilterString("foo:!=:10", context="py", type="int")
        assert fs.match("11")
        fs = FilterString("foo:neq:10", context="py", type="int")
        assert fs.match(11)
        fs = FilterString("foo:!=:10", context="py", type="int")
        assert fs.match_fields({"foo": 11})

    def test_filter_string_re(self):
        fs = FilterString("foo:re:.*bar.*", context="py")
        assert fs.match("babar")
        fs = FilterString("foo:~:.*bar.*", context="py")
        assert fs.match("babar")

    def test_filter_string_lk(self):
        fs = FilterString(r"foo:lk:%bar%", context="py")
        assert fs.match("babars")
        assert not fs.match("babar")
        fs = FilterString(r"foo:%:%bar%", context="py")
        assert fs.match("babars")
        assert not fs.match("babar")

    def test_filter_string_sw(self):
        fs = FilterString(r"foo:sw:bar", context="py")
        assert fs.match("barroom")
        fs = FilterString(r"foo:->:bar", context="py")
        assert fs.match("barroom")

    def test_filter_string_ew(self):
        fs = FilterString(r"foo:ew:bar", context="py")
        assert fs.match("babar")
        fs = FilterString(r"foo:<-:bar", context="py")
        assert fs.match("babar")

    def test_filter_string_in(self):

        fs = FilterString(r"foo:in:bar,baz", context="py")
        assert fs.match("bar")
        assert fs.match("baz")
        assert not fs.match("uqbar")

        fs = FilterString(r"foo:[]:bar,baz", context="py")
        assert fs.match("bar")
        assert fs.match("baz")
        assert not fs.match("uqbar")

    def test_filter_string_nin(self):

        fs = FilterString(r"foo:nin:bar,baz", context="py")
        assert not fs.match("bar")
        assert not fs.match("baz")
        assert fs.match("uqbar")

        fs = FilterString(r"foo:![]:bar,baz", context="py")
        assert not fs.match("bar")
        assert not fs.match("baz")
        assert fs.match("uqbar")

    def test_filter_string_bt(self):

        fs = FilterString(r"foo:bt:10,20", context="py", type="int")
        assert fs.match(15)
        assert fs.match("17")
        assert not fs.match(21)

        fs = FilterString(r"foo:bt:10,20", context="py", type="int")
        assert fs.match(15)
        assert fs.match("17")
        assert fs.match(20)  # between is inclusive
        assert not fs.match(21)

    def test_filter_string_fz(self):

        fs = FilterString("foo:fz:abels", context="py", type="text")
        assert fs.match("abelson", fuzz=0.8)
        assert not fs.match("abelson", fuzz=0.99)


if __name__ == "__main__":
    unittest.main()
