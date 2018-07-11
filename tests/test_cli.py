import os
import sys

# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
# from cli import get_options

class argParseTestCase(unittest.TestCase):
    def test_parser(self):
        options = get_options(['-f', 'config.yaml'])
        self.assertEquals('config.yaml', options.config)