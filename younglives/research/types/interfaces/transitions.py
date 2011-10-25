import datetime

from zope.interface import Interface
from zope import schema

from collective.wfform import _

class IWorkflowForm(Interface):
    """Utility to present a z3c.form during a workflow transition
    """

class IDeadlineTransition(Interface):

    new_deadline = schema.Date(
        title=_(u"New Internal Deadline"),
        description=_(u"Leave this blank to keep the original internal deadline, the new internal deadline will be added to the change comment"),
        required=False)
