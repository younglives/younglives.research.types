import datetime

from zope.component import getMultiAdapter, getUtility
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import ILocalPortletAssignmentManager
from plone.portlets.constants import CONTEXT_CATEGORY

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

class ResearchDatabaseView(BrowserView):  

    template = ViewPageTemplateFile('templates/research_database_view.pt')

    def __call__(self):
        portletManager  = getUtility(IPortletManager, name='plone.leftcolumn')
        assignable = getMultiAdapter((self.context, portletManager,), ILocalPortletAssignmentManager)
        assignable.setBlacklistStatus(CONTEXT_CATEGORY, True)
        return self.template() 

    def getStateInfo(self, state):
        portal_workflow = getToolByName(self, 'portal_workflow')
        research_workflow = portal_workflow.getWorkflowById('research_workflow')
        state = research_workflow['states'][state]
        return state

    def getPapersByYear(self):
        """Return the papers in reverse order by ref no"""
        portal_catalog = getToolByName(self, 'research_database_catalog')
        results = portal_catalog(portal_type='Research',
                                 sort_on='sortable_id',
                                 sort_order='reverse')
        return results

    def getNextYear(self):
        """Return the next year to do the year labels in the template"""
        now = datetime.datetime.now()
        next_year = now.year + 1
        return str(next_year)[2:]
