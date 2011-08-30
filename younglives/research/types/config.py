from Products.Archetypes.atapi import DisplayList

PROJECTNAME = 'younglives.research.types'

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
    ('J', 'Journal article'),
    ('TN', 'Technical Note'),
    ('PP', 'Policy Paper'),
    ('PB', 'Policy Brief'),
    ('SP', 'Student Paper'),
    ('BC', 'Book Chapter'),
    ('O', 'Other'),
))

PAPER_ORIGIN = DisplayList((
    ('student_call', 'Student Call for Papers'),
    ('internal', 'YL team/Internal'),
    ('external_commision', 'External commission'),
    ('student_ad_hoc', 'Student Ad Hoc'),
    ('vietnam_call', 'Vietnam Call for Papers'),
    ('ethiopia_external', 'Ethiopia external commission'),
    ('other', 'Other'),
))
