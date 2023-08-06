# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import iaweb.mosaic


class IawebMosaicLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=iaweb.mosaic)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'iaweb.mosaic:default')


IAWEB_MOSAIC_FIXTURE = IawebMosaicLayer()


IAWEB_MOSAIC_INTEGRATION_TESTING = IntegrationTesting(
    bases=(IAWEB_MOSAIC_FIXTURE,),
    name='IawebMosaicLayer:IntegrationTesting',
)


IAWEB_MOSAIC_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(IAWEB_MOSAIC_FIXTURE,),
    name='IawebMosaicLayer:FunctionalTesting',
)


IAWEB_MOSAIC_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        IAWEB_MOSAIC_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='IawebMosaicLayer:AcceptanceTesting',
)
