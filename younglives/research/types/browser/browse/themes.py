from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName

from younglives.research.types.config import RESEARCH_THEME

class BrowseThemesView(BrowserView):
    """View to browse the research database by themes"""

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.request.set('disable_border', True)
        self.selectedTheme = self.request.form.get('theme') or None

    def title(self):
        return 'Browsing by Research Theme'

    def content(self):
        if self.selectedTheme is None:
            return
        catalog = getToolByName(self.context, 'portal_catalog')
        return catalog({
            'meta_type': 'Research',
            'theme': self.selectedTheme,
            'sort_on': 'sortable_title',
        })

    def getThemesVocab(self):
        return RESEARCH_THEME
