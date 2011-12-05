import time
import unittest2 as unittest
from zExceptions import BadRequest

from zope.component import getSiteManager

from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

from Products.CMFCore.utils import getToolByName

from base import YOUNGLIVES_RESEARCH_TYPES_INTEGRATION_TESTING

class TestWorkflow(unittest.TestCase):
    """Test workflow configuration"""
    layer = YOUNGLIVES_RESEARCH_TYPES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.workflow = getToolByName(self.portal, 'portal_workflow')
        self.research_workflow = self.workflow.getWorkflowById('research_workflow')

    def testStatesExist(self):
        research_workflow = self.research_workflow
        all_states = research_workflow['states'].objectIds()
        assert len(all_states) == 12
        assert '09_completed' in all_states
        assert '03_initial-draft' in all_states
        assert '04_draft' in all_states
        assert '06_external-review' in all_states
        assert '10_in-production' in all_states
        assert '05_internal-review' in all_states
        assert '07_journal-submission' in all_states
        assert '08_journal-review' in all_states
        assert '01_planned' in all_states
        assert '02_proposed' in all_states
        assert '12_published' in all_states
        assert '11_rejected' in all_states

    def testTransitionsExist(self):
        research_workflow = self.research_workflow
        all_transitions = research_workflow['transitions'].objectIds()
        assert 'accept' in all_transitions
        assert 'accept_draft' in all_transitions
        assert 'complete' in all_transitions
        assert 'decline' in all_transitions
        assert 'external-review' in all_transitions
        assert 'internal-review' in all_transitions
        assert 'note' in all_transitions
        assert 'journal-review' in all_transitions
        assert 'journal-submission' in all_transitions
        assert 'produce' in all_transitions
        assert 'propose' in all_transitions
        assert 'publish' in all_transitions
        assert 'redraft' in all_transitions
        assert 'reject' in all_transitions
        assert 'retrieve' in all_transitions
        assert len(all_transitions) == 15, len(all_transitions)

class TestWorkflowStates(unittest.TestCase):
    """Test workflow states have correct transitions"""
    layer = YOUNGLIVES_RESEARCH_TYPES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.workflow = getToolByName(self.portal, 'portal_workflow')
        self.research_workflow = self.workflow.getWorkflowById('research_workflow')
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('ResearchDatabase', 'rd1')
        self.rd1 = getattr(self.portal, 'rd1')
        self.rd1.invokeFactory('Research', 'r1')
        self.r1 = getattr(self.rd1, 'r1')

    def testPlannedState(self):
        r1 = self.r1
        object_state = self.workflow.getInfoFor(r1, 'review_state')
        self.assertEqual('01_planned', object_state)
        transitions = self.workflow['research_workflow'].states['01_planned'].getTransitions()
        assert 'accept' in transitions
        assert 'accept_draft' in transitions
        assert 'journal-review' in transitions
        assert 'propose' in transitions
        assert 'reject' in transitions
        assert 'note' in transitions
        assert len(transitions) == 6

    def testProposedState(self):
        r1 = self.r1
        self.workflow.doActionFor(r1, 'propose')
        object_state = self.workflow.getInfoFor(r1, 'review_state')
        self.assertEqual('02_proposed', object_state)
        transitions = self.workflow['research_workflow'].states['02_proposed'].getTransitions()
        assert 'reject' in transitions
        assert 'accept' in transitions
        assert 'accept_draft' in transitions
        assert 'decline' in transitions
        assert 'journal-review' in transitions
        assert 'note' in transitions
        assert len(transitions) == 6

    def testInitialDraftState(self):
        transitions = self.workflow['research_workflow'].states['03_initial-draft'].getTransitions()
        assert 'accept' in transitions
        assert 'reject' in transitions
        assert 'note' in transitions
        assert len(transitions) == 3

    def testDraftState(self):
        transitions = self.workflow['research_workflow'].states['04_draft'].getTransitions()
        assert 'internal-review' in transitions
        assert 'journal-submission' in transitions
        assert 'external-review' in transitions
        assert 'note' in transitions
        assert len(transitions) == 4

    def testInternalReviewState(self):
        transitions = self.workflow['research_workflow'].states['05_internal-review'].getTransitions()
        assert 'complete' in transitions
        assert 'reject' in transitions
        assert 'redraft' in transitions
        assert 'note' in transitions
        assert len(transitions) == 4

    def testExternalReviewState(self):
        transitions = self.workflow['research_workflow'].states['06_external-review'].getTransitions()
        assert 'complete' in transitions
        assert 'reject' in transitions
        assert 'redraft' in transitions
        assert 'note' in transitions
        assert len(transitions) == 4

    def testCompletedState(self):
        transitions = self.workflow['research_workflow'].states['09_completed'].getTransitions()
        assert 'reject' in transitions
        assert 'produce' in transitions
        assert 'note' in transitions
        assert len(transitions) == 3

    def testInProductionState(self):
        transitions = self.workflow['research_workflow'].states['10_in-production'].getTransitions()
        assert 'reject' in transitions
        assert 'publish' in transitions
        assert 'note' in transitions
        assert len(transitions) == 3

    def testPublishedState(self):
        transitions = self.workflow['research_workflow'].states['12_published'].getTransitions()
        assert len(transitions) == 0

    def testJournalSubmissionState(self):
        transitions = self.workflow['research_workflow'].states['07_journal-submission'].getTransitions()
        assert 'journal-review' in transitions
        assert 'reject' in transitions
        assert 'redraft' in transitions
        assert 'note' in transitions
        assert len(transitions) == 4

    def testJournalReviewState(self):
        transitions = self.workflow['research_workflow'].states['08_journal-review'].getTransitions()
        assert 'complete' in transitions
        assert 'publish' in transitions
        assert 'reject' in transitions
        assert 'note' in transitions
        assert len(transitions) == 4

    def testRejectedState(self):
        transitions = self.workflow['research_workflow'].states['11_rejected'].getTransitions()
        assert 'retrieve' in transitions
        assert 'note' in transitions
        assert len(transitions) == 2
