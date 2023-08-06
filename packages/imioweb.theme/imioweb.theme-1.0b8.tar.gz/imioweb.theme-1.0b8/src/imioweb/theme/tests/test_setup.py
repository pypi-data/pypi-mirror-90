# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from imioweb.theme.testing import IMIOWEB_THEME_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that imioweb.theme is properly installed."""

    layer = IMIOWEB_THEME_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if imioweb.theme is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'imioweb.theme'))

    def test_browserlayer(self):
        """Test that IImiowebThemeLayer is registered."""
        from imioweb.theme.interfaces import (
            IImiowebThemeLayer)
        from plone.browserlayer import utils
        self.assertIn(IImiowebThemeLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = IMIOWEB_THEME_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(username=TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['imioweb.theme'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if imioweb.theme is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'imioweb.theme'))

    def test_browserlayer_removed(self):
        """Test that IImiowebThemeLayer is removed."""
        from imioweb.theme.interfaces import \
            IImiowebThemeLayer
        from plone.browserlayer import utils
        self.assertNotIn(
            IImiowebThemeLayer,
            utils.registered_layers(),
        )
