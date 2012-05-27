import datetime

from zope.component import getMultiAdapter, getUtility
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import ILocalPortletAssignmentManager
from plone.portlets.constants import CONTEXT_CATEGORY

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from younglives.research.types.config import RESEARCH_COUNTRY,\
                                             RESEARCH_METHODOLOGY,\
                                             RESEARCH_THEME

class ResearchFolderView(BrowserView):  

    template = ViewPageTemplateFile('templates/research_folder_view.pt')

    def __call__(self):
        portletManager  = getUtility(IPortletManager, name='plone.leftcolumn')
        assignable = getMultiAdapter((self.context, portletManager,), ILocalPortletAssignmentManager)
        assignable.setBlacklistStatus(CONTEXT_CATEGORY, True)
        return self.template() 

    def searchResearch(self):
        """Return a list of research items from the faceted search
        """
        request = self.request
        research_catalog = getToolByName(self, 'research_database_catalog')
        if hasattr(self.request, 'research_theme'):
            research_theme = getattr(self.request, 'research_theme')
        else:
            research_theme = self.vocabResearchTheme().keys()
        if hasattr(self.request, 'research_methodology'):
            research_methodology = getattr(self.request, 'research_methodology')
        else:
            research_methodology = self.vocabResearchMethodology().keys()
        if hasattr(self.request, 'research_country'):
            research_country = getattr(self.request, 'research_country')
        else:
            research_country = self.vocabResearchCountry().keys()
        research_items = research_catalog(theme=research_theme,
                                          methodology=research_methodology,
                                          country=research_country,
                                          sort_on='id')
        return research_items

    def vocabResearchTheme(self):
        """Get the vocab for the research thene
        """
        return RESEARCH_THEME

    def vocabResearchMethodology(self):
        """Get the vocab for the research methodology
        """
        return RESEARCH_METHODOLOGY

    def vocabResearchCountry(self):
        """Get the vocab for the research country
        """
        return RESEARCH_COUNTRY
