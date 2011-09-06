import datetime

from zope.interface import Interface
from zope import schema

from collective.wfform import _

class IWorkflowForm(Interface):
    """Utility to present a z3c.form during a workflow transition
    """

class IComment(Interface):

    comment = schema.Text(
        title=_(u"Comment"),
        description=_(u"Please enter a comment for this state change."),
        required=False)

class IProposedTransition(Interface):

    test_field = schema.Text(
        title=_(u"Testing"),
        description=_(u"This is a test."),
        required=True)

class IAcceptTransition(Interface):

    field = schema.Date(
        title=_(u"A date field"),
        description=_(u"This isn't saved anywhere yet"),
        #default=datetime.date(2007, 4, 1),
        required=True)
