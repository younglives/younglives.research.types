import unittest2 as unittest

from base import YOUNGLIVES_RESEARCH_TYPES_INTEGRATION_TESTING

class TestContentType(unittest.TestCase):
    """Test content type"""
    layer = YOUNGLIVES_RESEARCH_TYPES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
