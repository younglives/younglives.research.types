import os
import transaction
from AccessControl import ClassSecurityInfo
from DateTime.DateTime import DateTime
from DateTime.DateTime import DateError
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
                                             PAPER_MANAGER, \
                                             PAPER_ORIGIN

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
            print new_id
            object = self[new_id]
            object.setReferenceNumber(fields[0][1:-1])
            # authors
            authors = fields[1][1:-1]
            authors = self._importAuthors(authors)
            object.setPaperAuthor(authors[0])
            if len(authors) > 1:
                object.setCoAuthors(authors[1:])
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
            # paper state
            self._createState(object, fields[8][1:-1], fields[9][1:-1], fields)
            # cell 14, Paper origin
            origin = fields[14][1:-1]
            if origin in PAPER_ORIGIN.values():
                origin_key = PAPER_ORIGIN.getKey(origin)
                object.setResearchOrigin(origin_key)
            next_deadline = self._getNextDeadline(object, fields)
            if next_deadline:
                object.setNextDeadline(next_deadline)
            # deadlines
            if fields[22]:
                object.setFirstDraftDeadline(fields[22])
            if fields[28]:
                object.setSecondDraftDeadline(fields[28])
            if fields[34]:
                object.setFinalDraftDeadline(fields[34])
            # contracts comments
            if fields[17]:
                object.setContractsComment(fields[17])
            # data release comments
            if fields[21]:
                object.setDataReleaseAgreement(fields[21])
            # Private comment from final column
            if fields[37]:
                data = '<p>' + fields[37] + '</p>'
                object.setPrivateNotes(data)
            object.unmarkCreationFlag()
            object.reindexObject()
            transaction.savepoint(optimistic = True)
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

    def _createState(self, object, state, comment, fields):
        """Move the object to the right state"""
        default_comment = 'Automatic transition during intitial import.'
        wf_tool = getToolByName(self, 'portal_workflow')
        # Pending proposal and [Blank] OR N/A should be initial state
        if state == 'Withdrawn/On hold':
            wf_tool.doActionFor(object, 'reject', comment=comment)
            return
        if state not in ['Proposal under review',
                         'Pending 1st draft',
                         'Draft under review',
                         'Pending next draft',
                         'Pending final draft',
                         'Final draft received',
                         'Pending journal submission',
                         'Pending journal review',
                         'Completed',
                         'In production',
                         'Published',
                         ]:
            if comment != 'N/A':
                wf_tool.doActionFor(object, 'note', comment=comment)
            return
        if state == 'Proposal under review':
            wf_tool.doActionFor(object, 'propose', comment=comment)
            return
        if fields[13]:
            new_comment = fields[13][1:-1]
        else:
            new_comment = default_comment
        wf_tool.doActionFor(object, 'propose', comment=new_comment)
        if state == 'Pending 1st draft':
            wf_tool.doActionFor(object, 'accept', comment=comment)
            return
        wf_tool.doActionFor(object, 'accept', comment=default_comment)
        if fields[27]:
            wf_tool.doActionFor(object, 'internal-review', comment=default_comment)
            wf_tool.doActionFor(object, 'redraft', comment=fields[27][1:-1])            
        if fields[33]:
            wf_tool.doActionFor(object, 'external-review', comment=default_comment)
            wf_tool.doActionFor(object, 'redraft', comment=fields[33][1:-1])            
        if state in ['Pending next draft', 'Pending final draft']:
            return
        # journal review and journal submission are currently the same state
        if state == 'Pending journal submission':
            wf_tool.doActionFor(object, 'journal-submission', comment=comment)
            return
        if state == 'Pending journal review':
            wf_tool.doActionFor(object, 'journal-submission', comment=comment)
            wf_tool.doActionFor(object, 'journal-review', comment=comment)
            return
        if state == 'Draft under review':
            wf_tool.doActionFor(object, 'internal-review', comment=comment)
            return
        wf_tool.doActionFor(object, 'internal-review', comment=default_comment)
        if state == 'Completed':
            wf_tool.doActionFor(object, 'complete', comment=comment)
            return
        if fields[36]:
            new_comment = fields[36][1:-1]
        else:
            new_comment = default_comment
        wf_tool.doActionFor(object, 'complete', comment=new_comment)
        if state == 'In production':
            wf_tool.doActionFor(object, 'produce', comment=comment)
            return
        wf_tool.doActionFor(object, 'produce', comment=default_comment)
        if state == 'Published':
            wf_tool.doActionFor(object, 'publish', comment=comment)
        return

    def _getNextDeadline(self, object, fields):
        """Work out the next deadline from the date fields"""
        dates = []
        for field_num in [10, 11, 12, 15, 16, 18, 19, 20, 22, 23, 24, 25, 25, 28, 29, 30, 31, 32, 34, 35]:
            date = fields[field_num]
            try:
                DateTime(date)
            except (DateTime.SyntaxError, DateError):
                pass
            else:
                dates.append(DateTime(date))
        last_date = marker = DateTime()-5000
        for date in dates:
            if date > last_date:
                last_date = date
        if last_date != marker:
            return last_date
        #due = fields[10]
        #rcvd = fields[11]
        #accept = fields[12]
        #sent = fields[15]
        #rcvd4 = fields[16]
        #sent2 = fields[18]
        #rcvd6 = fields[19]
        #data_released = fields[20]
        #due3 = fields[22] - first draft due date
        #rcvd2 = fields[23]
        #sent_review = fields[24]
        #rcvd_review = fields[25]
        #sent_author = fields[26]
        #due4 = fields[28] - second draft due date
        #rcvd3 = fields[29]
        #sent_review2 = fields[30]
        #rcvd_review2 = fields[31]
        #sent_author2 = fields[32]
        #due2 = fields[34 - final due date
        #rcvd5 = fields[35]

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
