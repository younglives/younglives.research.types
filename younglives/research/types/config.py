from Products.Archetypes.atapi import DisplayList

GLOBALS = globals()
PROJECTNAME = 'younglives.research.types'
SKINS_DIR = 'skins'

ADD_PERMISSIONS = {
    'Research': 'YounglivesResearchTypes: Add Research',
    'ResearchDatabase': 'YounglivesResearchTypes: Add ResearchDatabase',
}

RESEARCH_THEME = DisplayList((
    ('1', 'Theme 1: Dynamics of poverty'),
    ('2', 'Theme 2: Children\'s experiences of poverty'),
    ('3', 'Theme 3: Learning, time use and life transitions'),
    ('M', 'Methodology'),
    ('X', 'Cross-cutting (e.g., gender, inequalities)'),
    ('N/A', 'N/A'),
))

RESEARCH_METHODOLOGY = DisplayList((
    ('', 'N/A'),
    ('MM', 'Mixed methods'),
    ('QL', 'Qualitative methods'),
    ('QN', 'Quantitative methods'),
))

RESEARCH_COUNTRY = DisplayList((
    ('ETH', 'Ethiopia'), # E in original spreadsheet
    ('IND', 'India'), # I in original spreadsheet
    ('PER', 'Peru'), # P in original spreadsheet
    ('VNM', 'Vietnam'), # V in original spreadsheet
))

RESEARCH_OUTPUT = DisplayList((
    ('WP', 'Working Paper'),
    ('J', 'Journal Article'),
    ('TN', 'Technical Note'),
    ('PP', 'Policy Paper'),
    ('PB', 'Policy Brief'),
    ('SP', 'Student Paper'),
    ('BC', 'Book Chapter'),
    ('O', 'Other'),
))

PAPER_ORIGIN = DisplayList((
    ('external_commision', 'External commissioned'),
    ('external_non_commision', 'External non-commissioned'),
    ('student_commision', 'Student commissioned'),
    ('student_non_commision', 'Student non-commissioned'),
    ('internal', 'YL team/internal'),
    ('other', 'Other'),
))

# vocabs for initial imports 

PAPER_MANAGER = DisplayList((
    ('Caroline', 'caroline.knowles@qeh.ox.ac.uk'),
    ('Paul', 'pauldornan'),
    ('Emma', 'emma.merry@qeh.ox.ac.uk'),
    ('Inka', 'inkabarnett'),
    ('Caine', 'cainerolleston'),
    ('Andreas', 'andreasgeorgiadis'),
    ('Ginny', 'virginiamorrow'),
    ('Martin', 'martinwoodhead'),
    ('Abhijeet', 'abhijeetsingh'),
    ('Sofya', 'sofyakrutikova'),
    ('Kirrily', 'kirrilypells'),
    ('Michelle', 'michelle.chew@qeh.ox.ac.uk'),
))


"""
ginacrivello
helenmurray
joboyden
melaniefrost
stefandercon
tassewwoldehanna
#
worknehyadete
"""