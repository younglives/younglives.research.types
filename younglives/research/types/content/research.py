from AccessControl import ClassSecurityInfo
from zope.interface import implements

from Products.Archetypes.atapi import registerType
from Products.ATContentTypes.content.base import ATCTContent
from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName

from younglives.research.types import permissions
from younglives.research.types.config import PROJECTNAME
from younglives.research.types.interfaces.research import IResearch

from schemata import ResearchSchema

class Research(ATCTContent):
    """A piece of research"""

    security = ClassSecurityInfo()

    implements(IResearch)

    meta_type = 'Research'
    _at_rename_after_creation = True

    schema = ResearchSchema

# Edit form helper methods

    security.declareProtected(permissions.ModifyPortalContent, 'getCurrentUser')
    def getCurrentUser(self):
        """
        Get the currrently logged in user."""
        mtool = getToolByName(self, 'portal_membership')
        current_user = mtool.getAuthenticatedMember()
        return current_user.getId()

    security.declareProtected(permissions.View, 'getPaperManagerFullName')
    def getPaperManagerFullName(self):
        """
        Get the full name of the assigned to user."""
        user_id = self.getAssignedTo()
        if user_id is None:
            return
        mtool = getToolByName(self, 'portal_membership')
        user = mtool.getMemberInfo(user_id)
        if user is None:
            # user deleted, just return the id
            return user_id
        user_name = user['fullname']
        return user_name

# view helper methods

    security.declareProtected(permissions.View, 'getPaperMembersVocab')
    def getPaperMembersVocab(self):
        """Return the member of the group, as a display list"""
        return self.aq_inner.aq_parent.getPaperMembersVocab()

registerType(Research, PROJECTNAME)
