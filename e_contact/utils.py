import logging

from django.conf import settings

try:
    from twilio.rest import Client
    have_twilio = True
except ImportError:
    have_twilio = False

from .models import Contact

logger = logging.getLogger(__name__)

DEFAULT_CONTACT_SETTINGS = {
    'twilio-account-sid': None,
    'twilio-auth-token': None,
    'sms-from': None,
    'sms-to': None,
    'sms-body': 'New contact request received',
}


def notify():
    """
    This should be called periodically to notify the admin of any contacts
    that need to be processed.
    """
    # Twilio is the only currently-implemented notification mechanism.
    if not have_twilio:
        logger.critical('Contact notify() should not be called if Twilio isn\'t available!')
        return

    contact_settings = DEFAULT_CONTACT_SETTINGS.copy()
    if hasattr(settings, 'CONTACT_SETTINGS'):
        contact_settings.update(settings.CONTACT_SETTINGS)

    if not all(
            (
                contact_settings['twilio-account-sid'],
                contact_settings['twilio-auth-token'],
                contact_settings['sms-from'],
                contact_settings['sms-to'],
            )
    ):
        logger.critical('Contact notify() should not be called if twilio isn\'t configured!')
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
        client = Client(contact_settings['twilio-account-sid'], contact_settings['twilio-auth-token'])
        message = client.messages.create(
            to=contact_settings['sms-to'],
            from_=contact_settings['sms-from'],
            body=contact_settings['sms-body'],
        )
        logger.info(
            'Result: error_code %r, error_message %r, price %r, status %s',
            message.error_code, message.error_message, message.price,
            message.status
        )
    else:
        logger.info('No contact requests require notification.')
