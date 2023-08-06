# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.CMFPlone.utils import get_installer
from iaweb.mosaic.testing import IAWEB_MOSAIC_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that iaweb.mosaic is properly installed."""

    layer = IAWEB_MOSAIC_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = get_installer(self.portal, self.layer['request'])

    def test_product_installed(self):
        """Test if iaweb.mosaic is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'iaweb.mosaic'))

    def test_browserlayer(self):
        """Test that IIawebMosaicLayer is registered."""
        from iaweb.mosaic.interfaces import (
            IIawebMosaicLayer)
        from plone.browserlayer import utils
        self.assertIn(
            IIawebMosaicLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = IAWEB_MOSAIC_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = get_installer(self.portal, self.layer['request'])
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['iaweb.mosaic'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if iaweb.mosaic is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'iaweb.mosaic'))

    def test_browserlayer_removed(self):
        """Test that IIawebMosaicLayer is removed."""
        from iaweb.mosaic.interfaces import \
            IIawebMosaicLayer
        from plone.browserlayer import utils
        self.assertNotIn(
            IIawebMosaicLayer,
            utils.registered_layers())
