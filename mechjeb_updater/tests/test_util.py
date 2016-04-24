from unittest import TestCase

import util

class TestUtil(TestCase):
    def test_is_string(self):
        s = "util.makeString()"
        self.assertTrue(isinstance(s, basestring))
