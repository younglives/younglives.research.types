import unittest2 as unittest

from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

from base import YOUNGLIVES_RESEARCH_TYPES_INTEGRATION_TESTING

class TestContentType(unittest.TestCase):
    """Test content type"""
    layer = YOUNGLIVES_RESEARCH_TYPES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def testAddType(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('ResearchDatabase', 'rd1')
        rd1 = getattr(self.portal, 'rd1')
        assert 'rd1' in self.portal.objectIds()
