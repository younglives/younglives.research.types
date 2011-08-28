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
        self.workflow = getToolByName(self.portal, 'portal_workflow')
        self.research_workflow = self.workflow.getWorkflowById('research_workflow')

    def testStatesExist(self):
        research_workflow = self.research_workflow
        all_states = research_workflow['states'].objectIds()
        assert 'completed' in all_states

    def testTransitionsExist(self):
        research_workflow = self.research_workflow
        all_transitions = research_workflow['transitions'].objectIds()
        assert 'complete' in all_transitions
