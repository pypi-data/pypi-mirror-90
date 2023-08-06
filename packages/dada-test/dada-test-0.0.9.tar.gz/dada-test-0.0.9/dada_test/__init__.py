import os
import unittest

FIXTURES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "fixtures"))


class BaseTest(unittest.TestCase):
    def get_fixture(self, p):
        """absolute path to a fixture"""
        return os.path.join(FIXTURES_DIR, p)
