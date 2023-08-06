import os
import logging
import unittest

from dada_test import BaseTest
from dada_types import T


class TypeHumTests(BaseTest):
    def test_hum_display_byes(self):
        """
        Test int <-> text converstion / generation
        """
        assert T.byte_size.hum(1024) == "1.0 KB"
        assert T.byte_size.hum(1024.0) == "1.0 KB"


if __name__ == "__main__":
    unittest.main()
