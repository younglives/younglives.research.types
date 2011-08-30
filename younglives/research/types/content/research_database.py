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

# spreadsheet upload methods

    security.declareProtected(permissions.ManagePortal, 'processFile')
    def processFile(self):
        """process the file"""
        input = self._openFile()
        # skip the first 7 lines, as these are headers
        input = input[7:]
        import pdb;pdb.set_trace()
        for line in input:
            fields = line.split('|')
            if len(fields) == 1:
                continue
            if fields[1] == '':
                # assume anything that does not have an author is not a record
                continue
            new_id = self.invokeFactory('Research', fields[0][1:-1])
            object = self[new_id]
            object.unmarkCreationFlag()
        return input

    def _openFile(self):
        """open the file, and return the file contents"""
        data_path = os.path.abspath('var')
        try:
            data_catch = open(data_path + '/spreadsheet', 'rU')
        except IOError: # file does not exist, or path is wrong
            try:
                # we might be in foreground mode
                data_path = os.path.abspath('../var')
                data_catch = open(data_path + '/spreadsheet', 'rU')
            except IOError: # file does not exist, or path is wrong
                return 'File does not exist'
        input = data_catch.read()
        data_catch.close()
        input = input.replace("'", "\\'\\")
        input = input.split('\n')
        return input

registerType(ResearchDatabase, PROJECTNAME)
