from unittest import mock

from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase

from e_contact.utils import notify
from e_contact.models import Contact


EMAIL_CONTACT_SETTINGS = {
    'email-subject': 'foo',
    'email-body': 'foo',
    'email-from': 'joe@example.com',
    'email-to': 'joe@example.com',
}


class TestNotify(TestCase):

    def test_notify_when_some_ready_but_nothing_configured(self):
        Contact.objects.create(
            name='Joe Example',
            email='joe@example.com',
            message='Example message',
        )
        with self.assertRaises(ImproperlyConfigured):
            notify()

    @mock.patch('e_contact.utils.send_mail')
    def test_notify_when_configured_but_none_ready(self, mock_send_mail):
        with self.settings(
            CONTACT_SETTINGS=EMAIL_CONTACT_SETTINGS,
            EMAIL_HOST='smtp.example.com',
        ):
            self.assertEquals(notify(), 0)
        self.assertFalse(mock_send_mail.called)

    @mock.patch('e_contact.utils.send_mail')
    def test_notify_when_configured_and_some_ready(self, mock_send_mail):
        Contact.objects.create(
            name='Joe Example',
            email='joe@example.com',
            message='Example message',
        )
        with self.settings(
            CONTACT_SETTINGS=EMAIL_CONTACT_SETTINGS,
            EMAIL_HOST='smtp.example.com',
        ):
            self.assertEquals(notify(), 1)
        self.assertTrue(mock_send_mail.called)
