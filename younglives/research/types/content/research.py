import transaction
from AccessControl import ClassSecurityInfo
from zExceptions import BadRequest
from zope.interface import implements

from Products.Archetypes.atapi import registerType
from Products.ATContentTypes.content.base import ATCTContent
from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName

from younglives.research.types import _
from younglives.research.types import permissions
from younglives.research.types.config import PROJECTNAME
from younglives.research.types.interfaces.research import IResearch

from schemata import ResearchSchema

class Research(ATCTContent):
    """A piece of research"""

    security = ClassSecurityInfo()

    implements(IResearch)

    meta_type = 'Research'
    _at_rename_after_creation = False

    schema = ResearchSchema

    security.declarePrivate('at_post_create_script')
    def at_post_create_script(self):
        """change the id based on referenceNumber"""
        transaction.savepoint(optimistic = True)
        self.setId(self.getReferenceNumber())

    security.declarePrivate('at_post_edit_script')
    def at_post_edit_script(self):
        """change the id based on referenceNumber"""
        transaction.savepoint(optimistic = True)
        self.setId(self.getReferenceNumber())

# Edit form helper methods

    security.declareProtected(permissions.ModifyPortalContent, 'post_validate')
    def post_validate(self, REQUEST=None, errors=None):
        """Do the complex validation for the edit form"""
        form = REQUEST.form
        if errors is None:
            errors = {}
        referenceNumber = form.get('referenceNumber', None)
        if referenceNumber != self.getId():
            try:
                self.aq_parent._checkId(referenceNumber)
            except BadRequest:
                if referenceNumber in self.aq_parent.objectIds():
                    errors['referenceNumber'] = u'This reference number already exists.'
                else:
                    errors['referenceNumber'] = u'This is not a valid reference number.'
        return errors

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

# transition forms

    security.declareProtected(permissions.ModifyPortalContent, 'getSchemaForTransition')
    def getSchemaForTransition(self, transition):
        """Return a fieldset depending on the transition"""
        if transition == 'propose':
            from younglives.research.types.interfaces.transitions import IProposedTransition
            return IProposedTransition
        else:
            from younglives.research.types.interfaces.transitions import IAcceptTransition
            return IAcceptTransition

    security.declareProtected(permissions.ModifyPortalContent, 'processTransitionForm')
    def processTransitionForm(self, data):
        """Return a fieldset depending on the transition"""
        if data.has_key('test_field'):
            self.setDescription(data['test_field'])

registerType(Research, PROJECTNAME)
