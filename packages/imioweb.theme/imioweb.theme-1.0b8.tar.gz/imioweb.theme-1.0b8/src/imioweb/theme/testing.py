# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import imioweb.theme


class ImiowebThemeLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=imioweb.theme)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'imioweb.theme:default')


IMIOWEB_THEME_FIXTURE = ImiowebThemeLayer()


IMIOWEB_THEME_INTEGRATION_TESTING = IntegrationTesting(
    bases=(IMIOWEB_THEME_FIXTURE,),
    name='ImiowebThemeLayer:IntegrationTesting'
)


IMIOWEB_THEME_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(IMIOWEB_THEME_FIXTURE,),
    name='ImiowebThemeLayer:FunctionalTesting'
)


IMIOWEB_THEME_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        IMIOWEB_THEME_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='ImiowebThemeLayer:AcceptanceTesting'
)
