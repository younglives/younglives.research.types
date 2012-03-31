import string
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

    security.declareProtected(permissions.View, 'getLastComment')
    def getLastComment(self):
        """Return the last workflow comment"""
        workflow_tool = getToolByName(self, 'portal_workflow')
        history = workflow_tool.getInfoFor(self, 'review_history')
        if not history:
            return 'Initial record'
        last_comment = history[-1]['comments']
        if not last_comment:
            return 'Initial record'
        return last_comment

    security.declareProtected(permissions.View, 'sortable_id')
    def sortable_id(self):
        """Return the id so it sorts correctly"""
        id = self.getId()
        if len(id) != 8:
            # not a standard id, so ignore
            return id
        letter = id[-1:].lower()
        string_alphabet = string.ascii_lowercase
        list_alphabet = []
        list_alphabet.extend(string_alphabet)
        reverse_list_alphabet = list(list_alphabet)
        reverse_list_alphabet.reverse()
        # this is a generator object, so needs to be iterated over
        for i in (i for i,x in enumerate(list_alphabet) if x == letter):
            index = i
        new_letter = reverse_list_alphabet[index]
        return id[:7] + new_letter

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
        """Return the full name of the paper manager"""
        user_id = self.getField('paperManager').get(self)
        if user_id is None or user_id == '':
            return 'N/A'
        mtool = getToolByName(self, 'portal_membership')
        user = mtool.getMemberInfo(user_id)
        if user is None:
            # TODO: user deleted
            return user_id
        user_name = user['fullname']
        return user_name

    security.declareProtected(permissions.View, 'getPaperManagerFirstName')
    def getPaperManagerFirstName(self):
        """Return the first name of the paper manager"""
        full_name = self.getPaperManagerFullName()
        names = full_name.split(' ')
        return names[0]

    security.declareProtected(permissions.ModifyPortalContent, 'refStartUpDir')
    def refStartUpDir(self):
        """
        Get the authors folder path for the reference fields."""
        catalog = getToolByName(self, 'portal_catalog')
        # we could be in portal factory, so assume there is only one research database
        # and therefore only one authors folder
        authors = catalog(meta_type='AuthorFolder')
        if not authors:
            portal = getToolByName(self, 'portal_url')
            portal = portal.getPortalObject()
            return portal.absolute_url()
        path = catalog(meta_type='AuthorFolder')[0].getPath()
        return path

# view helper methods

    security.declareProtected(permissions.View, 'Title')
    def Title(self, **kw):
        """We have to override Title here to insert the reference number"""
        title = self.getField('title').get(self)
        reference_no = self.getReferenceNumber()
        if reference_no:
            return reference_no + ": " + title
        return title

    security.declareProtected(permissions.View, 'getTitle')
    def getTitle(self):
        """return the title, or raw title if in edit form"""
        obj = self
        # check if in edit form
        if string.split(self.REQUEST.PATH_INFO, '/')[-1:]  ==  ['edit']:
            return self.getField('title').get(self)
        return obj.Title()

    security.declareProtected(permissions.View, 'getTitle')
    def rawTitle(self):
        """return the raw title, where the reference number is not required"""
        title = self.getField('title').get(self)
        return title

    security.declareProtected(permissions.View, 'listAuthors')
    def listAuthors(self, family_first=True, all=True):
        """Return all the authors as a list of author objects"""
        authors = []
        author = self.getPaperAuthor()
        if author:
            authors.append(author)
        co_authors = self.getCoAuthors()
        for co_author in co_authors:
            authors.append(co_author)
        return authors

    security.declareProtected(permissions.View, 'getAllAuthors')
    def getAllAuthors(self, family_first=True, all=True):
        """Return all the authors as a text string"""
        authors = []
        author = self.getPaperAuthor()
        if author is None:
            authors.append('Undefined Author')
        elif family_first and not author.getNameOrder():
            authors.append(author.getFamilyName() + ', ' + author.getPersonalNames())
        else:
            authors.append(author.Title())
        co_authors = self.getCoAuthors()
        if not all and len(co_authors) > 2:
            return authors[0] + ' et al'
        for co_author in co_authors:
            if co_author is None:
                authors.append('Undefined Author')
            elif family_first and not co_author.getNameOrder():
                authors.append(co_author.getFamilyName() + ', ' + co_author.getPersonalNames())
            else:
                authors.append(co_author.Title())
        if family_first:
            return '; '.join(authors)
        return ', '.join(authors)

    security.declareProtected(permissions.View, 'getShortAuthors')
    def getShortAuthors(self):
        return self.getAllAuthors(all=False)

    security.declareProtected(permissions.View, 'getPaperMembersVocab')
    def getPaperMembersVocab(self):
        """Return the member of the group, as a display list"""
        return self.aq_inner.aq_parent.getPaperMembersVocab()

    def getWorkflowTitle(self):
        """Return the title of the current workflow state"""
        workflow_tool = getToolByName(self, 'portal_workflow')
        workflow = workflow_tool.getWorkflowById('research_workflow')
        current_state = workflow_tool.getInfoFor(self, 'review_state')
        state = workflow.states[current_state]
        return state.title

# transition forms

    security.declareProtected(permissions.ModifyPortalContent, 'getSchemaForTransition')
    def getSchemaForTransition(self, transition):
        """Return a fieldset depending on the transition"""
        if transition in ['note', 'propose', 'accept']:
            from younglives.research.types.interfaces.transitions import IDeadlineTransition
            return IDeadlineTransition
        elif transition in ['note', 'propose']:
            from younglives.research.types.interfaces.transitions import IDeadlineTransition
            return IDeadlineTransition
        else:
            # just the comment field
            return

    security.declareProtected(permissions.ModifyPortalContent, 'processTransitionForm')
    def processTransitionForm(self, data):
        """Process the transition forms"""
        comment = data['comment']
        if data.has_key('new_deadline'):
            if comment:
                comment = comment + ' '
            else:
                comment = ''
            if self.getNextDeadline():
                comment += 'Deadline changed from ' + self.getNextDeadline().strftime('%d/%m/%Y') + ' to '
            else:
                comment += 'Deadline set to '
            comment += data['new_deadline'].strftime('%d/%m/%Y')
            comment += '.'
            data['comment'] = comment
            self.setNextDeadline(data['new_deadline'].strftime('%Y/%m/%d'))
        return data

registerType(Research, PROJECTNAME)
