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
        assert len(all_states) == 11
        assert 'completed' in all_states
        assert 'draft' in all_states
        assert 'external-review' in all_states
        assert 'in-production' in all_states
        assert 'internal-review' in all_states
        assert 'peer-review' in all_states
        assert 'planned' in all_states
        assert 'propsosed' in all_states
        assert 'published' in all_states
        assert 'rejected' in all_states
        assert 'unpublished' in all_states

    def testTransitionsExist(self):
        research_workflow = self.research_workflow
        all_transitions = research_workflow['transitions'].objectIds()
        assert len(all_transitions) == 13
        assert 'accept' in all_transitions
        assert 'complete' in all_transitions
        assert 'deline' in all_transitions
        assert 'external-review' in all_transitions
        assert 'internal-review' in all_transitions
        assert 'peer-review' in all_transitions
        assert 'produce' in all_transitions
        assert 'propose' in all_transitions
        assert 'publish' in all_transitions
        assert 'redraft' in all_transitions
        assert 'refused' in all_transitions
        assert 'reject' in all_transitions
        assert 'retrieve' in all_transitions
