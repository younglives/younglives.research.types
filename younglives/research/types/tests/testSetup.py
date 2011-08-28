import time
import unittest2 as unittest
from zExceptions import BadRequest

from zope.component import getSiteManager

from Products.CMFCore.utils import getToolByName

from base import YOUNGLIVES_RESEARCH_TYPES_INTEGRATION_TESTING

class TestInstallation(unittest.TestCase):
    """Ensure product is properly installed"""
    layer = YOUNGLIVES_RESEARCH_TYPES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def testTypesInstalled(self):
        portal_types = getToolByName(self.portal, 'portal_types')
        assert 'Research' in portal_types.objectIds(), portal_types.objectIds()
        assert 'ResearchDatabase' in portal_types.objectIds(), portal_types.objectIds()

    def testPortalFactorySetup(self):
        assert 'Research' in self.portal.portal_factory.getFactoryTypes()
        assert 'ResearchDatabase' in self.portal.portal_factory.getFactoryTypes()

    def testWorkflowsInstalled(self):
        workflow_ids = self.portal.portal_workflow.getWorkflowIds()
        assert 'research_workflow' in workflow_ids

    def testWorkflowsMapped(self):
        workflows = self.portal.portal_workflow.getChainForPortalType('Research')
        assert ('research_workflow',) == workflows

class TestReinstall(unittest.TestCase):
    """Ensure product can be reinstalled safely"""
    layer = YOUNGLIVES_RESEARCH_TYPES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def testReinstall(self):
        portal_setup = getToolByName(self.portal, 'portal_setup')
        try:
            portal_setup.runAllImportStepsFromProfile('profile-younglives.research.types:default')
        except BadRequest:
            # if tests run too fast, duplicate profile import id makes test fail
            time.sleep(0.5)
            portal_setup.runAllImportStepsFromProfile('profile-younglives.research.types:default')
