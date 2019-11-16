from abc import ABC, abstractmethod
import logging

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.mail import send_mail

try:
    from twilio.rest import Client
    have_twilio = True
except ImportError:
    have_twilio = False

from .models import Contact

logger = logging.getLogger(__name__)

DEFAULT_CONTACT_SETTINGS = {
    # For sending SMS...
    'twilio-account-sid': None,
    'twilio-auth-token': None,
    'sms-from': None,
    'sms-to': None,
    'sms-body': 'New contact request received',

    # For sending e-mail...
    'email-subject': 'New contact request received',
    'email-body': 'New contact request received',
    'email-from': None,
    'email-to': None,
}


class Notifier(ABC):

    def __init__(self, contact_settings):
        self.contact_settings = contact_settings
        self.enabled = False
        self._determine_if_enabled()
        if self.enabled:
            if self._determine_if_misconfigured():
                raise ImproperlyConfigured(
                    f'{self.__class__.__name__} is not configured properly'
                )

    @abstractmethod
    def _determine_if_enabled(self):
        pass

    @abstractmethod
    def _determine_if_misconfigured(self):
        pass

    @abstractmethod
    def notify(self):
        pass

    def notify_if_enabled(self):
        if self.enabled:
            self.notify()


class TwilioNotifier(Notifier):

    def _determine_if_enabled(self):
        self.enabled = self.contact_settings['twilio-account-sid']

    def _determine_if_misconfigured(self):
        assert self.enabled

        if not have_twilio:
            logger.critical('Twilio isn\'t available!')
            return True

        return not all(
            (
                self.contact_settings['twilio-account-sid'],
                self.contact_settings['twilio-auth-token'],
                self.contact_settings['sms-from'],
                self.contact_settings['sms-to'],
            )
        )

    def notify(self):
        assert self.enabled

        client = Client(
            self.contact_settings['twilio-account-sid'],
            self.contact_settings['twilio-auth-token']
        )
        message = client.messages.create(
            to=self.contact_settings['sms-to'],
            from_=self.contact_settings['sms-from'],
            body=self.contact_settings['sms-body'],
        )
        logger.info(
            'Result: error_code %r, error_message %r, price %r, status %s',
            message.error_code, message.error_message, message.price,
            message.status
        )


class EmailNotifier(Notifier):

    def _determine_if_enabled(self):
        return self.contact_settings['email-to']

    def _determine_if_misconfigured(self):
        assert self.enabled

        if not settings.get('EMAIL_HOST'):
            return True

        return not all(
            (
                self.contact_settings['email-subject'],
                self.contact_settings['email-body'],
                self.contact_settings['email-from'],
                self.contact_settings['email-to'],
            )
        )

    def enabled(self):
        return self.enabled

    def notify(self):
        send_mail(
            self.contact_settings['email-subject'],
            self.contact_settings['email-body'],
            self.contact_settings['email-from'],
            [self.contact_settings['email-to']],
            fail_silently=False,
        )


def notify():
    """
    This should be called periodically to notify the admin of any contacts
    that need to be processed.
    """
    contact_settings = DEFAULT_CONTACT_SETTINGS.copy()
    if hasattr(settings, 'CONTACT_SETTINGS'):
        contact_settings.update(settings.CONTACT_SETTINGS)

    twilio = TwilioNotifier(contact_settings)
    email = EmailNotifier(contact_settings)

    if (twilio.enabled or email.enabled) is False:
        logger.critical(
            'Contact notify() should not be called if SMS or e-mail isn\'t configured!'
        )
        return

    # Currently there's no way to verify contact requests, so we
    # notify for requests in state SUBMITTED.
    initial_state = Contact.SUBMITTED
    final_state = Contact.NOTIFIED
    updated = Contact.objects.filter(
        state=initial_state
    ).update(state=final_state)
    if updated:
        logger.info('%d contact requests require notification.', updated)
        twilio.notify_if_enabled()
        email.notify_if_enabled()
    else:
        logger.info('No contact requests require notification.')
    return updated
