"""Tests for certbot.eff."""
from __future__ import unicode_literals
import unittest

import mock

from certbot import constants
from certbot.tests import util


class HandleSubscriptionTest(unittest.TestCase):
    """Tests for certbot.eff.handle_subscription."""
    def setUp(self):
        self.email = 'certbot@example.org'
        self.config = mock.Mock(email=self.email, eff_email=None)

    def _call(self):
        from certbot.eff import handle_subscription
        return handle_subscription(self.config)

    @util.patch_get_utility()
    @mock.patch('certbot.eff.subscribe')
    def test_failure(self, mock_subscribe, mock_get_utility):
        self.config.email = None
        self.config.eff_email = True
        self._call()
        self.assertFalse(mock_subscribe.called)
        self.assertFalse(mock_get_utility().yesno.called)
        actual = mock_get_utility().add_message.call_args[0][0]
        expected_part = "because you didn't provide an e-mail address"
        self.assertTrue(expected_part in actual)

    @mock.patch('certbot.eff.subscribe')
    def test_no_subscribe_with_no_prompt(self, mock_subscribe):
        self.config.eff_email = False
        with util.patch_get_utility() as mock_get_utility:
            self._call()
        self.assertFalse(mock_subscribe.called)
        self._assert_no_get_utility_calls(mock_get_utility)

    @util.patch_get_utility()
    @mock.patch('certbot.eff.subscribe')
    def test_subscribe_with_no_prompt(self, mock_subscribe, mock_get_utility):
        self.config.eff_email = True
        self._call()
        self._assert_subscribed(mock_subscribe)
        self._assert_no_get_utility_calls(mock_get_utility)

    def _assert_no_get_utility_calls(self, mock_get_utility):
        self.assertFalse(mock_get_utility().yesno.called)
        self.assertFalse(mock_get_utility().add_message.called)

    @util.patch_get_utility()
    @mock.patch('certbot.eff.subscribe')
    def test_subscribe_with_prompt(self, mock_subscribe, mock_get_utility):
        mock_get_utility().yesno.return_value = True
        self._call()
        self._assert_subscribed(mock_subscribe)
        self.assertFalse(mock_get_utility().add_message.called)
        self._assert_correct_yesno_call(mock_get_utility)

    def _assert_subscribed(self, mock_subscribe):
        self.assertTrue(mock_subscribe.called)
        self.assertEqual(mock_subscribe.call_args[0][0], self.email)

    @util.patch_get_utility()
    @mock.patch('certbot.eff.subscribe')
    def test_no_subscribe_with_prompt(self, mock_subscribe, mock_get_utility):
        mock_get_utility().yesno.return_value = False
        self._call()
        self.assertFalse(mock_subscribe.called)
        self.assertFalse(mock_get_utility().add_message.called)
        self._assert_correct_yesno_call(mock_get_utility)

    def _assert_correct_yesno_call(self, mock_get_utility):
        self.assertTrue(mock_get_utility().yesno.called)
        call_args, call_kwargs = mock_get_utility().yesno.call_args
        actual = call_args[0]
        expected_part = 'Electronic Frontier Foundation'
        self.assertTrue(expected_part in actual)
        self.assertFalse(call_kwargs.get('default', True))


class SubscribeTest(unittest.TestCase):
    """Tests for certbot.eff.subscribe."""
    def setUp(self):
        self.email = 'certbot@example.org'
        self.json = {'status': True}
        self.response = mock.Mock(ok=True)
        self.response.json.return_value = self.json

    @mock.patch('certbot.eff.requests.post')
    def _call(self, mock_post):
        mock_post.return_value = self.response

        from certbot.eff import subscribe
        subscribe(self.email)
        self._check_post_call(mock_post)

    def _check_post_call(self, mock_post):
        self.assertEqual(mock_post.call_count, 1)
        call_args, call_kwargs = mock_post.call_args
        self.assertEqual(call_args[0], constants.EFF_SUBSCRIBE_URI)

        data = call_kwargs.get('data')
        self.assertFalse(data is None)
        self.assertEqual(data.get('email'), self.email)

    @util.patch_get_utility()
    def test_bad_status(self, mock_get_utility):
        self.json['status'] = False
        self._call()  # pylint: disable=no-value-for-parameter
        actual = self._get_reported_message(mock_get_utility)
        expected_part = 'because your e-mail address appears to be invalid.'
        self.assertTrue(expected_part in actual)

    @util.patch_get_utility()
    def test_not_ok(self, mock_get_utility):
        self.response.ok = False
        self._call()  # pylint: disable=no-value-for-parameter
        actual = self._get_reported_message(mock_get_utility)
        unexpected_part = 'because'
        self.assertFalse(unexpected_part in actual)

    def _get_reported_message(self, mock_get_utility):
        self.assertTrue(mock_get_utility().add_message.called)
        return mock_get_utility().add_message.call_args[0][0]

    @util.patch_get_utility()
    def test_subscribe(self, mock_get_utility):
        self._call()  # pylint: disable=no-value-for-parameter
        self.assertFalse(mock_get_utility.called)


if __name__ == '__main__':
    unittest.main()  # pragma: no cover
