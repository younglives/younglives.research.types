import logging

from Products.CMFCore.utils import getToolByName
from Products.CMFEditions.setuphandlers import DEFAULT_POLICIES

def setVersionedTypes(portal, logger):
    portal_repository = getToolByName(portal, 'portal_repository')
    versionable_types = list(portal_repository.getVersionableContentTypes())
    type_id = 'Research'
    if type_id not in versionable_types:
        # use append() to make sure we don't overwrite any
        # content-types which may already be under version control
        versionable_types.append(type_id)
        # Add default versioning policies to the versioned type
        for policy_id in DEFAULT_POLICIES:
            portal_repository.addPolicyForContentType(type_id, policy_id)
    portal_repository.setVersionableContentTypes(versionable_types)

def setupVarious(context):

    if context.readDataFile('younglives.research.types_various.txt') is None:
        return
    logger = context.getLogger('younglives.research.types')
    site = context.getSite()
    setVersionedTypes(site, logger)
