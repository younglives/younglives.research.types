from plone.app.folder.folder import ATFolderSchema

from Products.Archetypes.atapi import Schema

from Products.ATContentTypes.content.schemata import ATContentTypeSchema
from Products.ATContentTypes.content.schemata import finalizeATCTSchema

ResearchDatabaseSchema = ATFolderSchema.copy() + Schema((

))

ResearchSchema = ATContentTypeSchema.copy() + Schema((

))

finalizeATCTSchema(ResearchSchema)
