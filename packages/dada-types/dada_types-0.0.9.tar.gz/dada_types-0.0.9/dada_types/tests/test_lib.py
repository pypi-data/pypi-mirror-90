import os
import logging
import unittest

from dada_test import BaseTest
from dada_types import T


TEST_LOGGER = logging.getLogger()


class TypeLibTests(BaseTest):
    def test_int_to_text(self):
        """
        Test int <-> text converstion / generation
        """
        int_val = T.int.gen()
        text_val = T.text.validate(int_val)
        dump_val = T.text.dump(text_val)
        assert text_val == dump_val
        new_int_val = T.int.validate(dump_val)
        assert int_val == new_int_val

    def test_t_get(self):
        """
        Test Type fetching
        """
        assert T.get("text").__name__ == "text"
        assert T.get("text").__dada_type__ == "text"

    def test_t_gen(self):
        """
        Test Type fetching
        """
        text = T.text_256.gen()
        assert len(text) <= 256


if __name__ == "__main__":
    unittest.main()
