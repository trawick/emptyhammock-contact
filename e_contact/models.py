import uuid

from django.db import models


class Contact(models.Model):
    MAX_NAME_LEN = 80

    SUBMITTED = 'submitted'
    # submitter validation finished
    VERIFIED = 'verified'
    # site admins notified of existence
    NOTIFIED = 'notified'
    # site admins did something with it
    HANDLED = 'handled'

    STATE_CHOICES = (
        (SUBMITTED, SUBMITTED),
        (VERIFIED, VERIFIED),
        (NOTIFIED, NOTIFIED),
        (HANDLED, HANDLED),
    )
    MAX_STATE_LEN = max([len(s) for s, _ in STATE_CHOICES])

    name = models.CharField(blank=False, max_length=MAX_NAME_LEN)
    email = models.EmailField(blank=False)
    message = models.TextField(max_length=800, blank=False)
    notes = models.TextField('Administrator notes', max_length=2048, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    state = models.CharField(
        max_length=MAX_STATE_LEN, blank=False,
        choices=STATE_CHOICES, default=SUBMITTED
    )

    def __str__(self):
        return 'Contacted {} by {} ({})'.format(
            self.created_at, self.email, self.state,
        )
