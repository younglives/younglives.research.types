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
        rd1.invokeFactory('Research', 'r1')
        assert 'r1' in rd1.objectIds()

class TestContentSchema(unittest.TestCase):
    """Test content type schema"""
    layer = YOUNGLIVES_RESEARCH_TYPES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('ResearchDatabase', 'rd1')
        self.rd1 = getattr(self.portal, 'rd1')
        self.rd1.invokeFactory('Research', 'r1')
        self.r1 = getattr(self.rd1, 'r1')

    def testSchema(self):
        r1 = self.r1
        schema = r1.schema
        field_ids = schema.keys()
        assert 'referenceNumber' in field_ids
        reference_field = schema['referenceNumber']
