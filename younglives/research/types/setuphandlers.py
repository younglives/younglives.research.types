import logging

def setupVarious(context):

    if context.readDataFile('younglives.research.types_various.txt') is None:
        return
    logger = context.getLogger('younglives.research.types')
    site = context.getSite()
