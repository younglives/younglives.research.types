from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName

from younglives.research.types.config import RESEARCH_COUNTRY

class BrowseCountry(BrowserView):
    """View to browse the research database by country of data"""

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.request.set('disable_border', True)
        self.selectedCountry = self.request.form.get('country') or None

    def title(self):
        return 'Browsing by Country'

    def content(self):
        if self.selectedCountry is None:
            return
        catalog = getToolByName(self.context, 'portal_catalog')
        return catalog({
            'meta_type': 'Research',
            'country': self.selectedCountry,
            'sort_on': 'sortable_title',
        })

    def getVocab(self):
        return RESEARCH_COUNTRY
