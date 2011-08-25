from AccessControl import ClassSecurityInfo
from zope.interface import implements

from plone.app.folder.folder import ATFolder

from Products.Archetypes.atapi import registerType
from Products.CMFCore.utils import getToolByName

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

registerType(ResearchDatabase, PROJECTNAME)
