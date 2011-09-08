from Products.Archetypes.atapi import DisplayList

GLOBALS = globals()
PROJECTNAME = 'younglives.research.types'
SKINS_DIR = 'skins'

ADD_PERMISSIONS = {
    'Research': 'YounglivesResearchTypes: Add Research',
    'ResearchDatabase': 'YounglivesResearchTypes: Add ResearchDatabase',
}

RESEARCH_THEME = DisplayList((
    ('1', 'Dynamics of poverty'),
    ('2', 'Children\'s experiences of poverty'),
    ('3', 'Schooling, time use and life transitions'),
    ('M', 'Methodology'),
    ('X', 'Cross-cutting (e.g., gender, inequalities)'),
))

RESEARCH_METHODOLOGY = DisplayList((
    ('', 'Not applicable'),
    ('MM', 'Mixed Methods'),
    ('QL', 'Qualitative Methods'),
    ('QN', 'Quantitative Methods'),
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
    ('external_non_commision', 'External Non-commissioned'),
    ('external_commision', 'External Commissioned'),
    ('student_non_commision', 'Student Non-commissioned'),
    ('student_commision', 'Student Commissioned'),
    ('internal', 'YL Team/Internal'),
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