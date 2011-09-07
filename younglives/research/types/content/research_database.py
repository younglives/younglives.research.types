import os
from AccessControl import ClassSecurityInfo
from zope.interface import implements

from plone.app.folder.folder import ATFolder

from Products.Archetypes.atapi import DisplayList
from Products.Archetypes.atapi import registerType
from Products.CMFCore.utils import getToolByName

from younglives.research.types import permissions
from younglives.research.types.config import PROJECTNAME
from younglives.research.types.interfaces.research_database import IResearchDatabase

from schemata import ResearchDatabaseSchema

# only need the vocab imports for the initial import
from younglives.research.types.config import RESEARCH_THEME, \
                                             RESEARCH_METHODOLOGY, \
                                             RESEARCH_COUNTRY, \
                                             RESEARCH_OUTPUT, \
                                             PAPER_MANAGER

class ResearchDatabase(ATFolder):
    """Research database"""

    security = ClassSecurityInfo()

    implements(IResearchDatabase)

    meta_type = 'ResearchDatabase'
    _at_rename_after_creation = True

    schema = ResearchDatabaseSchema

    security.declarePublic('canSetConstrainTypes')
    def canSetConstrainTypes(self):
        return False

    security.declareProtected(permissions.View, 'getPaperMembersVocab')
    def getPaperMembersVocab(self):
        """Return the members of the paper manager group, as a display list"""
        group_tool = getToolByName(self, 'portal_groups')
        if not self.getPaperManagerGroup():
            return self.getMembersVocab()
        portal_group = group_tool.getGroupById(self.getPaperManagerGroup())
        group_members = portal_group.getGroupMembers()
        vocab = DisplayList()
        for member in group_members:
            if member.getProperty('fullname'):
                vocab.add(member.getProperty('id'),member.getProperty('fullname'))
            else:
                vocab.add(member.getProperty('id'),member.getProperty('id'))
        return vocab

    security.declareProtected(permissions.ModifyPortalContent, 'getPortalGroupsVocab')
    def getPortalGroupsVocab(self):
        """Return the portal groups, as a display list"""
        group_tool = getToolByName(self, 'portal_groups')
        portal_groups = group_tool.listGroups()
        vocab = DisplayList()
        vocab.add('', 'Use all portal Members')
        for group in portal_groups:
            if group.getProperty('title'):
                vocab.add(group.getProperty('id'),group.getProperty('title'))
            else:
                vocab.add(group.getProperty('id'),group.getProperty('id'))
        return vocab

    security.declareProtected(permissions.ModifyPortalContent, 'getMembersVocab')
    def getMembersVocab(self):
        """Get the members available as a DisplayList."""
        m_tool = getToolByName(self, 'portal_membership')
        users = m_tool.searchForMembers()
        vocab = DisplayList()
        for user in users:
            user_id = user.getId()
            user_name = user.getProperty('fullname')
            vocab.add(user_id, user_name)
        return vocab

# view methods

    security.declareProtected(permissions.View, 'getPapersByAuthors')
    def getPapersByAuthors(self):
        """Return the papers sorted by author family name"""
        portal_catalog = getToolByName(self, 'portal_catalog')
        results = portal_catalog(meta_type='Author', sort_on='sortable_title')
        return results

    security.declareProtected(permissions.View, 'getPapersForAuthor')
    def getPapersForAuthor(self, author):
        """Return the papers sorted by author family name"""
        object = author.getObject()
        return object.getBRefs()

# spreadsheet upload methods

    security.declareProtected(permissions.ManagePortal, 'processFile')
    def processFile(self):
        """process the file"""
        input = self._openFile()
        # skip the first 7 lines, as these are headers
        input = input[7:]
        for line in input:
            fields = line.split('|')
            if len(fields) == 1:
                continue
            if fields[1] == '':
                # assume anything that does not have an author is not a record
                continue
            new_id = self.invokeFactory('Research', fields[0][1:-1])
            object = self[new_id]
            object.setReferenceNumber(fields[0][1:-1])
            # authors
            authors = fields[1][1:-1]
            authors = self._importAuthors(authors)
            object.setPrimaryAuthor(authors[0])
            if len(authors) > 1:
                object.setSecondaryAuthors(authors[1:])
            # title
            title = fields[2][1:-1].replace('""', '"')
            object.setTitle(title)
            # research theme
            themes = []
            theme = fields[3][1:-1]
            for char in theme:
                if char in ['1','2','3','M','X',]:
                    themes.append(char)
            object.setResearchTheme(themes)
            # research methodology
            methodology = fields[4][1:-1]
            if methodology in ['MM', 'QL', 'QN']:
                object.setResearchMethodology(methodology)
            # countries
            countries = []
            if 'E' in fields[5]:
                countries.append('ETH')
            if 'I' in fields[5]:
                countries.append('IND')
            if 'P' in fields[5]:
                countries.append('PER')
            if 'V' in fields[5]:
                countries.append('VNM')
            object.setResearchCountry(countries)
            # research output
            outputs = []
            output = fields[6][1:-1]
            for item in RESEARCH_OUTPUT:
                if item in output:
                    outputs.append(item)
            object.setResearchOutput(outputs)
            # paper manager
            manager = fields[7][1:-1]
            if manager in PAPER_MANAGER:
                object.setPaperManager(PAPER_MANAGER.getValue(manager))
            object.unmarkCreationFlag()
            object.reindexObject()
        return self

    def _importAuthors(self, authors):
        """Import the authors"""
        if 'authors' not in self.objectIds():
            new_id = self.invokeFactory('AuthorFolder', 'authors')
            object = self[new_id]
            workflow_tool = getToolByName(self, 'portal_workflow', None)
            workflow_tool.doActionFor(object,'publish',comment='Published on initial import')
        else:
            object = self['authors']
        return object._createAuthors(authors)

    def _openFile(self):
        """open the file, and return the file contents"""
        data_path = os.path.abspath('var')
        try:
            data_catch = open(data_path + '/spreadsheet.csv', 'rU')
        except IOError: # file does not exist, or path is wrong
            try:
                # we might be in foreground mode
                data_path = os.path.abspath('../var')
                data_catch = open(data_path + '/spreadsheet.csv', 'rU')
            except IOError: # file does not exist, or path is wrong
                return 'File does not exist'
        input = data_catch.read()
        data_catch.close()
        #input = input.replace("'", "\'\")
        input = input.split('\n')
        return input

registerType(ResearchDatabase, PROJECTNAME)
