from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName

from younglives.research.types.config import RESEARCH_THEME

class BrowsePaperManagersView(BrowserView):
    """View to browse the research database by paper managers"""

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.request.set('disable_border', True)
        self.selectedManager = self.request.form.get('paper_manager') or None

    def title(self):
        return 'Browsing by Paper Manager'

    def content(self):
        if self.selectedManager is None:
            return
        catalog = getToolByName(self.context, 'research_database_catalog')
        return catalog({
            'meta_type': 'Research',
            'paper_manager': self.selectedManager,
            'sort_on': 'sortable_title',
        })

    def getManagersVocab(self):
        return self.context.getPaperMembersVocab()
