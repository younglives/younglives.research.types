from AccessControl import ClassSecurityInfo
from zope.interface import implements

from Products.Archetypes.atapi import registerType
from Products.ATContentTypes.content.base import ATCTContent
from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName

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

registerType(Research, PROJECTNAME)
