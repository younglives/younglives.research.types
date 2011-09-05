from Products.Five.browser import BrowserView

class BrowseAuthorsView(BrowserView):
    """View to browse the research database by authors"""

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def title(self):
        return 'Browsing by Authors'

    def results(self):
        return self.context.getPapersByAuthors()

    def papersForAuthor(self, author):
        return self.context.getPapersForAuthor(author)
