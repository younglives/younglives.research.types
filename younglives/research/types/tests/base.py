from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting

from plone.testing import z2

class TestCase(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import younglives.research.types
        self.loadZCML(package=younglives.research.types)
        import collective.wfform
        self.loadZCML(package=collective.wfform)

        # Install product and call its initialize() function
        z2.installProduct(app, 'younglives.research.types')
        z2.installProduct(app, 'collective.wfform')

        # Note: you can skip this if my.product is not a Zope 2-style
        # product, i.e. it is not in the Products.* namespace and it
        # does not have a <five:registerPackage /> directive in its
        # configure.zcml.

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        self.applyProfile(portal, 'younglives.research.types:default')

    def tearDownZope(self, app):
        # Uninstall product
        z2.uninstallProduct(app, 'younglives.research.types')

        # Note: Again, you can skip this if my.product is not a Zope 2-
        # style product

YOUNGLIVES_RESEARCH_TYPES_FIXTURE = TestCase()
YOUNGLIVES_RESEARCH_TYPES_INTEGRATION_TESTING = IntegrationTesting(bases=(YOUNGLIVES_RESEARCH_TYPES_FIXTURE,), name="YounglivesResearchTypes:Integration")
