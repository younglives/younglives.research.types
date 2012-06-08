from zope.component import getMultiAdapter, getUtility
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import ILocalPortletAssignmentManager
from plone.portlets.constants import CONTEXT_CATEGORY

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from younglives.research.types.config import RESEARCH_THEME, \
                                             RESEARCH_METHODOLOGY, \
                                             RESEARCH_COUNTRY, \
                                             PAPER_ORIGIN

class ResearchSearch(BrowserView):  

    template = ViewPageTemplateFile('templates/research_search.pt')

    def __call__(self):
        portletManager  = getUtility(IPortletManager, name='plone.leftcolumn')
        assignable = getMultiAdapter((self.context, portletManager,), ILocalPortletAssignmentManager)
        assignable.setBlacklistStatus(CONTEXT_CATEGORY, True)
        return self.template()

    def searchOutputs(self):
        """Return the research outputs results as objects
        """
        request = self.request
        research_database_catalog = getToolByName(self, 'research_database_catalog')
        if hasattr(self.request, 'research_theme'):
            research_theme = getattr(self.request, 'research_theme')
        else:
            research_theme = self.uniqueValuesForResearchTheme()
        outputs = research_database_catalog(meta_type ='Research',
                                            theme = research_theme,
                                           )
        return outputs

    def vocabResearchTheme(self):
        """Get the vocab for the research theme
        """
        return RESEARCH_THEME

    def uniqueValuesForResearchTheme(self):
        """Get the list of values for the course availability facet
        """
        research_database_catalog = getToolByName(self, 'research_database_catalog')
        research_theme = research_database_catalog.uniqueValuesFor("theme")
        return research_theme
