from zope.i18nmessageid import MessageFactory

from Products.Archetypes import atapi
from Products.CMFCore import utils
from Products.CMFCore.DirectoryView import registerDirectory

from younglives.research.types import config
from younglives.research.types.config import GLOBALS,SKINS_DIR

_ = MessageFactory('younglives.research.types')

registerDirectory(SKINS_DIR, GLOBALS)

def initialize(context):
    """Initializer called when used as a Zope 2 product."""

    from content.research import Research
    from content.research_database import ResearchDatabase

    content_types, constructors, ftis = atapi.process_types(
        atapi.listTypes(config.PROJECTNAME),
        config.PROJECTNAME)

    for atype, constructor in zip(content_types, constructors):
        utils.ContentInit('%s: %s' % (config.PROJECTNAME, atype.portal_type),
            content_types=(atype, ),
            permission=config.ADD_PERMISSIONS[atype.portal_type],
            extra_constructors=(constructor,),
            ).initialize(context)
