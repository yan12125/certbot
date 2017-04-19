"""ACME utilities."""

from __future__ import unicode_literals

import six


def map_keys(dikt, func):
    """Map dictionary keys."""
    return dict((func(key), value) for key, value in six.iteritems(dikt))


def openssl_digest_name(digest):
    """A wrapper for digest names for pyOpenSSL.
       It should be bytes on Python 2 and unicode on Python 3"""
    if six.PY3:  # pragma: no cover
        return digest
    else:
        return digest.encode("charmap")
