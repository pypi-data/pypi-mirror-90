# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import ideabox.theme


class IdeaboxThemeLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=ideabox.theme)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'ideabox.theme:default')


IDEABOX_THEME_FIXTURE = IdeaboxThemeLayer()


IDEABOX_THEME_INTEGRATION_TESTING = IntegrationTesting(
    bases=(IDEABOX_THEME_FIXTURE,),
    name='IdeaboxThemeLayer:IntegrationTesting',
)


IDEABOX_THEME_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(IDEABOX_THEME_FIXTURE,),
    name='IdeaboxThemeLayer:FunctionalTesting',
)


IDEABOX_THEME_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        IDEABOX_THEME_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='IdeaboxThemeLayer:AcceptanceTesting',
)
