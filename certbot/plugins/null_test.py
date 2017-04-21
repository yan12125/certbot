"""Tests for certbot.plugins.null."""
from __future__ import unicode_literals
import unittest

import mock
import six


class InstallerTest(unittest.TestCase):
    """Tests for certbot.plugins.null.Installer."""

    def setUp(self):
        from certbot.plugins.null import Installer
        self.installer = Installer(config=mock.MagicMock(), name="null")

    def test_it(self):
        self.assertTrue(isinstance(self.installer.more_info(), six.text_type))
        self.assertEqual([], self.installer.get_all_names())
        self.assertEqual([], self.installer.supported_enhancements())


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
