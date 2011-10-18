from Acquisition import aq_inner
from DateTime import DateTime
from random import choice
from zope.component import getMultiAdapter
from zope.formlib import form
from zope.interface import implements

from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _

from younglives.research.types.browser.portlets.interfaces import IReportsPortlet

class Assignment(base.Assignment):
    implements(IReportsPortlet)

    def __init__(self):
        pass

    @property
    def title(self):
        return _(u"Report Links")

class AddForm(base.AddForm):
    form_fields = form.Fields(IReportsPortlet)
    label = _(u"Add Research Reports Links Portlet")
    description = _(u"This portlet displays links to reports.")

    def create(self, data):
        return Assignment()

class EditForm(base.EditForm):
    form_fields = form.Fields(IReportsPortlet)
    label = _(u"Add Research Reports Links Portlet")
    description = _(u"This portlet displays links to reports.")

class Renderer(base.Renderer):
    _template = ViewPageTemplateFile('reports.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

        context = aq_inner(self.context)
        portal_state = getMultiAdapter((context, self.request), name=u'plone_portal_state')
        self.anonymous = portal_state.anonymous()  # whether or not the current user is Anonymous
        self.portal_url = portal_state.portal_url()  # the URL of the portal object
        
        # a list of portal types considered "end user" types
        self.typesToShow = portal_state.friendly_types()  

        plone_tools = getMultiAdapter((context, self.request), name=u'plone_tools')
        self.catalog = plone_tools.catalog()

    def render(self):
        return self._template()
