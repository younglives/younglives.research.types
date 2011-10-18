from archetypes.referencebrowserwidget import ReferenceBrowserWidget
from plone.app.folder.folder import ATFolderSchema

from Products.Archetypes.atapi import CalendarWidget
from Products.Archetypes.atapi import DateTimeField
from Products.Archetypes.atapi import LinesField
from Products.Archetypes.atapi import MultiSelectionWidget
from Products.Archetypes.atapi import ReferenceField
from Products.Archetypes.atapi import Schema
from Products.Archetypes.atapi import SelectionWidget
from Products.Archetypes.atapi import StringField
from Products.Archetypes.atapi import StringWidget
from Products.Archetypes.atapi import TextField
from Products.Archetypes.atapi import RichWidget

from Products.ATContentTypes.content.schemata import ATContentTypeSchema
from Products.ATContentTypes.content.schemata import finalizeATCTSchema

from younglives.research.types.config import RESEARCH_THEME, \
                                             RESEARCH_METHODOLOGY, \
                                             RESEARCH_COUNTRY, \
                                             RESEARCH_OUTPUT, \
                                             PAPER_ORIGIN

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

    ReferenceField('paperAuthor',
        allowed_types = ['Author',],
        relationship = 'Author',
        searchable = 0,
        required = 0,
        widget = ReferenceBrowserWidget(
            label = "Author",
            startup_directory_method = 'refStartUpDir',
            show_review_state = True,
        ),
    ),

    ReferenceField('coAuthors',
        allowed_types = ['Author',],
        relationship = 'coAuthor',
        searchable = 0,
        required = 0,
        multiValued = 1,
        widget = ReferenceBrowserWidget(
            label = "Co-authors",
            startup_directory_method = 'refStartUpDir',
            show_review_state = True,
        ),
    ),

    LinesField('researchTheme',
        required = False,
        searchable = False,
        vocabulary = RESEARCH_THEME,
        multiValued = True,
        widget = MultiSelectionWidget(
            label='Research Theme',
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
            label='Research Methodology',
            format='radio',
        )
    ),

    LinesField('researchOutput',
        required = False,
        searchable = False,
        vocabulary = RESEARCH_OUTPUT,
        multiValued = True,
        widget = MultiSelectionWidget(
            label='Research Output',
            format='checkbox',
        )
    ),

    StringField('researchOrigin',
        required = 0,
        searchable = 0,
        vocabulary = PAPER_ORIGIN,
        widget = SelectionWidget(
            label = 'Paper Origin',
        ),
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

    DateTimeField('nextDeadline',
        required = 0,
        searchable = 0,
        widget = CalendarWidget(
            label = 'Next Deadline',
            show_hm = False,
        ),
    ),

    DateTimeField('firstDraftDeadline',
        schemata='Deadlines',
        required = 0,
        searchable = 0,
        widget = CalendarWidget(
            label = 'First Draft Deadline',
            show_hm = False,
        ),
    ),

    DateTimeField('secondDraftDeadline',
        schemata='Deadlines',
        required = 0,
        searchable = 0,
        widget = CalendarWidget(
            label = 'Second Draft Deadline',
            show_hm = False,
        ),
    ),

    DateTimeField('finalDraftDeadline',
        schemata='Deadlines',
        required = 0,
        searchable = 0,
        widget = CalendarWidget(
            label = 'Final Draft Deadline',
            show_hm = False,
        ),
    ),

    StringField('dataReleaseAgreement',
        required = 0,
        searchable = 0,
        widget = StringWidget(
            label = 'Data Release Agreement',
        ),
    ),

    ReferenceField('relatedResearch',
        allowed_types = ['Research',],
        relationship = 'relatedResearch',
        searchable = 0,
        required = 0,
        multiValued = 1,
        widget = ReferenceBrowserWidget(
            label = "Related Outputs",
            show_review_state = True,
        ),
    ),

    TextField('privateNotes',
        required = False,
        searchable = False,
        validators = ('isTidyHtmlWithCleanup',),
        default_output_type = 'text/x-html-safe',
        widget = RichWidget(
            label = 'Private Notes',
            description = "Any notes stored here will only be available to system managers.",
            rows = 25,)
        ),

))

finalizeATCTSchema(ResearchSchema)
