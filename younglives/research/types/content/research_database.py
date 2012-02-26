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
from Products.CMFCore.WorkflowCore import WorkflowException

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

    def shortenTitle(self, title):
        """Shorten a title to appear in a tabular view"""
        if len(title) > 100:
            title = title[:100]
            word_list = title.split(' ')
            # strip off the last word/part word
            word_list = word_list[:-1]
            title = ' '.join(word_list)
            title = title + ' ...'
        return title

# spreadsheet upload methods

    security.declareProtected(permissions.ManagePortal, 'processFile')
    def processFile(self, testing=0):
        """process the file"""
        wf_tool = getToolByName(self, 'portal_workflow')
        count = 0
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
            try:
                # could be a single integer
                int(fields[3])
                themes.append(fields[3])
            except ValueError:
                # text string that probably has multiple values
                theme = fields[3][1:-1]
                for char in theme:
                    if char in ['1','2','3','M','X',]:
                        themes.append(char)
            object.setResearchTheme(themes)
            # research methodology
            methodology = fields[4][1:-1]
            if methodology[-1:] == '?':
                methodology = methodology[:-1]
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
            else:
                object.setPaperManager('')
            # paper state
            self._createState(object, fields[8][1:-1], fields)
            wf_tool.doActionFor(object, 'note', comment=fields[9][1:-1])
            # cell 14, Paper origin
            origin = fields[14][1:-1]
            origins = []
            for item in PAPER_ORIGIN:
                if PAPER_ORIGIN.getValue(item).lower() in origin.lower():
                    origins.append(item)
            object.setResearchOrigin(origins)
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
                object.setContractsComment(fields[17][1:-1])
            # data release comments
            if fields[21]:
                object.setDataReleaseAgreement(fields[21][1:-1])
            # Private comment from final column
            if fields[37]:
                data = '<p>' + fields[37][1:-1] + '</p>'
                object.setPrivateNotes(data)
            object.unmarkCreationFlag()
            object.reindexObject()
            transaction.savepoint(optimistic = True)
            count += 1
            if testing and int(testing) <= count:
                return self
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

    def _createState(self, object, state, fields):
        """Move the object to the right state"""
        default_comment = 'Automatic transition during initial import.'
        wf_tool = getToolByName(self, 'portal_workflow')
        # state 1 Planned
        if fields[10]:
            comment = 'Proposal due: ' + fields[10] + '.'
            wf_tool.doActionFor(object, 'note', comment=comment)
        if state in ['Pending proposal',]:
            return
        # state 2 Proposed
        if fields[11]:
            comment = 'Proposal accepted: ' + fields[11] + '.'
        else:
            comment = default_comment
        wf_tool.doActionFor(object, 'propose', comment=comment)
        if state in ['Proposal under review',]:
            return
        # state 3 Being drafted
        if fields[12]:
            comment = 'Proposal approved: ' + fields[12] + '.'
            wf_tool.doActionFor(object, 'accept_draft', comment=default_comment)
        if fields[13]:
            comment = fields[13][1:-1]
            wf_tool.doActionFor(object, 'note', comment=comment)
        if state in ['Pending 1st draft',]:
            return
        if fields[22]:
            comment = 'First draft due on: ' + fields[22] + '.'
            wf_tool.doActionFor(object, 'note', comment=comment)
        if fields[23]:
            comment = 'First draft received on: ' + fields[23] + '.'
            wf_tool.doActionFor(object, 'accept', comment=comment)
        else:
            wf_tool.doActionFor(object, 'accept', comment=default_comment)
        # state 5 Internal review (first review)
        if fields[24]:
            comment = 'First draft sent to reviewers on: ' + fields[24] + '.'
        else:
            comment = default_comment
        wf_tool.doActionFor(object, 'internal-review', comment=comment)
        if fields[25]:
            comment = 'First draft received from reviewers on: ' + fields[25] + '.'
            wf_tool.doActionFor(object, 'note', comment=comment)
        if fields[27]:
            comment = 'First draft comments/actions: ' + fields[27][1:-1] + '.'
            wf_tool.doActionFor(object, 'note', comment=comment)
        # state 4 Draft received
        if state in ['1st draft under review',]:
            return
        if fields[26]:
            comment = 'First draft comments sent to author on: ' + fields[26] + '.'
        else:
            comment = default_comment
        wf_tool.doActionFor(object, 'redraft', comment=default_comment)
        # state 6 External review (second review)
        if fields[28]:
            comment = 'Second draft due on: ' + fields[28] + '.'
            wf_tool.doActionFor(object, 'note', comment=comment)
        if fields[29]:
            comment = 'Second draft received on: ' + fields[29] + '.'
            wf_tool.doActionFor(object, 'note', comment=comment)
        if state in ['Pending 2nd draft',]:
            return
        if fields[30]:
            comment = 'Second draft sent to reviewers on: ' + fields[30] + '.'
        else:
            comment = default_comment
        wf_tool.doActionFor(object, 'external-review', comment=default_comment)
        if fields[31]:
            comment = 'Second draft received from reviewers on: ' + fields[31] + '.'
            wf_tool.doActionFor(object, 'note', comment=comment)
        if fields[33]:
            comment = 'Second draft comments/actions: ' + fields[33][1:-1] + '.'
            wf_tool.doActionFor(object, 'note', comment=comment)
        # state 4 Draft received
        if state in ['2nd draft under review',]:
            return
        if fields[32]:
            comment = 'Second draft comments sent to author on: ' + fields[32] + '.'
        else:
            comment = default_comment
        wf_tool.doActionFor(object, 'redraft', comment=default_comment)
        if fields[34]:
            comment = 'Final draft due on: ' + fields[34] + '.'
            wf_tool.doActionFor(object, 'note', comment=comment)
        if fields[35]:
            comment = 'Final draft received on: ' + fields[35] + '.'
            wf_tool.doActionFor(object, 'external-review', comment=comment)
        if fields[36]:
            comment = 'Final draft comments/actions: ' + fields[36][1:-1] + '.'
            try:
                wf_tool.doActionFor(object, 'redraft', comment=comment)
            except WorkflowException:
                # field 35 is empty so we're still in state 4
                wf_tool.doActionFor(object, 'external-review', comment=default_comment)
                wf_tool.doActionFor(object, 'redraft', comment=comment)
        if state in ['Pending final draft',]:
            return
        if state in ['Withdrawn/on hold',]:
            wf_tool.doActionFor(object, 'reject', comment=default_comment)
            return
        # state 7 and 8
        if state in ['Pending journal submission', 'Pending journal review']:
            wf_tool.doActionFor(object, 'journal-submission', comment=default_comment)
            if state in ['Pending journal review',]:
                wf_tool.doActionFor(object, 'journal-review', comment=default_comment)
            return
        # state 9 completed
        wf_tool.doActionFor(object, 'complete', comment=default_comment)
        if state in ['Completed',]:
            return
        # state 10 In production
        wf_tool.doActionFor(object, 'produce', comment=default_comment)
        if state in ['In production',]:
            return
        # state 12 Published
        wf_tool.doActionFor(object, 'publish', comment=default_comment)
        if state in ['Published',]:
            return
        # a state has not been handled
        print state

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

    def _openFile(self):
        """open the file, and return the file contents"""
        data_path = os.path.abspath('var')
        #data_path = os.path.abspath('/usr/local/plone/younglives/var')
        #data_path = os.path.abspath('/usr/home/mdavis/sites/young/var')
        try:
            data_catch = open(data_path + '/spreadsheet.csv', 'rU')
        except IOError:
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
