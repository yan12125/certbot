"""Tests for acme.jose.errors."""

from __future__ import unicode_literals

import re
import unittest


class UnrecognizedTypeErrorTest(unittest.TestCase):
    def setUp(self):
        from acme.jose.errors import UnrecognizedTypeError
        self.error = UnrecognizedTypeError('foo', {'type': 'foo'})

    def test_str(self):
        self.assertTrue(re.match(
            r"^foo was not recognized, full message: {u?'type': u?'foo'}$",
            str(self.error)))


if __name__ == '__main__':
    unittest.main()  # pragma: no cover
