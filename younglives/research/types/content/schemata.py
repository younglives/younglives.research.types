from plone.app.folder.folder import ATFolderSchema

from Products.Archetypes.atapi import LinesField
from Products.Archetypes.atapi import MultiSelectionWidget
from Products.Archetypes.atapi import ReferenceField
from Products.Archetypes.atapi import Schema
from Products.Archetypes.atapi import SelectionWidget
from Products.Archetypes.atapi import StringField
from Products.Archetypes.atapi import StringWidget

from Products.ATContentTypes.content.schemata import ATContentTypeSchema
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget

from younglives.research.types.config import RESEARCH_THEME, \
                                             RESEARCH_METHODOLOGY, \
                                             RESEARCH_COUNTRY, \
                                             RESEARCH_OUTPUT

ResearchDatabaseSchema = ATFolderSchema.copy() + Schema((

    StringField('paperManagerGroup',
        searchable = 0,
        required = 0,
        vocabulary = 'getPortalGroupsVocab',
        widget = SelectionWidget(
            label = 'Paper Managers',
            description = 'Please choose which user group contains the users for the paper managers.',
            ),
        ),

))

ResearchSchema = ATContentTypeSchema.copy() + Schema((

    StringField('referenceNumber',
        searchable = 0,
        required = 1,
        widget = StringWidget(
            label = 'Reference Number',
            description = 'This should be in the form of year-num-letter',
            ),
        ),

    ReferenceField('primaryAuthor',
        allowed_types = ['Author',],
        relationship = 'PrimaryAuthor',
        searchable = 0,
        required = 1,
        widget = ReferenceBrowserWidget(
            label = "Primary Author",
            startup_directory = 'authors',
            show_review_state = True,
        ),
    ),

    ReferenceField('secondaryAuthors',
        allowed_types = ['Author',],
        relationship = 'SecondaryAuthor',
        searchable = 0,
        required = 0,
        multiValued = 1,
        widget = ReferenceBrowserWidget(
            label = "Secondary Authors",
            startup_directory = 'authors',
            show_review_state = True,
        ),
    ),

    LinesField('researchTheme',
        required = False,
        searchable = False,
        vocabulary = RESEARCH_THEME,
        multiValued = True,
        widget = MultiSelectionWidget(
            label='Reasearch Theme',
            format='checkbox',
        )
    ),

    LinesField('researchCountry',
        required = False,
        searchable = False,
        vocabulary = RESEARCH_COUNTRY,
        multiValued = True,
        widget = MultiSelectionWidget(
            label='Country of data to be used',
            format='checkbox',
        )
    ),

    StringField('researchMethodology',
        required = False,
        searchable = False,
        vocabulary = RESEARCH_METHODOLOGY,
        widget = SelectionWidget(
            label='Reasearch Methodology',
            format='radio',
        )
    ),

    LinesField('researchOutput',
        required = False,
        searchable = False,
        vocabulary = RESEARCH_OUTPUT,
        multiValued = True,
        widget = MultiSelectionWidget(
            label='Reasearch Output',
            format='checkbox',
        )
    ),

    StringField('paperManager',
        required = 0,
        searchable = 0,
        vocabulary = 'getPaperMembersVocab',
        default_method = 'getCurrentUser',
        widget = SelectionWidget(
            label = 'Paper Manager',
        ),
    ),

))

finalizeATCTSchema(ResearchSchema)
