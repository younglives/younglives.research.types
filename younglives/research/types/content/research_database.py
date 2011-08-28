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

registerType(ResearchDatabase, PROJECTNAME)
