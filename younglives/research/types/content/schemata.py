from plone.app.folder.folder import ATFolderSchema

from Products.Archetypes.atapi import Schema

from Products.ATContentTypes.content.schemata import ATContentTypeSchema
from Products.ATContentTypes.content.schemata import finalizeATCTSchema

from younglives.research.types.config import RESEARCH_THEME, RESEARCH_METHODOLOGY, RESEARCH_COUNTRY, RESEARCH_OUTPUT

ResearchDatabaseSchema = ATFolderSchema.copy() + Schema((

))

ResearchSchema = ATContentTypeSchema.copy() + Schema((

    StringField('researchTheme',
        required = False,
        searchable = False,
        vocabulary = RESEARCH_THEME,
        multiValued = True,
        widget = SelectionWidget(
            label='Reasearch Theme',
        )
    ),

))

finalizeATCTSchema(ResearchSchema)
