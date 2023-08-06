# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import imio.patterns


class ImioPatternsLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=imio.patterns)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'imio.patterns:default')


IMIO_PATTERNS_FIXTURE = ImioPatternsLayer()


IMIO_PATTERNS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(IMIO_PATTERNS_FIXTURE,),
    name='ImioPatternsLayer:IntegrationTesting',
)


IMIO_PATTERNS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(IMIO_PATTERNS_FIXTURE,),
    name='ImioPatternsLayer:FunctionalTesting',
)


IMIO_PATTERNS_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        IMIO_PATTERNS_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='ImioPatternsLayer:AcceptanceTesting',
)
