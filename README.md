# emptyhammock-contact

Idiosyncratic contact form support for Django

Contact requests (messages) shouldn't simply generate e-mails; they should create
a representation in the database that supports identifying which messages
have been handled and adding notes pertinent to the contact request.

The administrator shouldn't be notified of a contact request until the e-mail has
been verified, since there's no way to respond to the submitter without a
working e-mail.  Contact requests with unverified e-mails should be
garbage-collected automatically.

## Near-term plans

Add these features before we can use it on a client site:

* SPAM-prevention
* E-mail validation (user must click on link to fix state of message in db)
* Notifying site admin when there are new contact form submissions that have
  been validated

## Integration requirements

* Add `e_contact` to `INSTALLED_APPS`.
* Include the URLs via `url(r'^contact/', include('e_contact.urls', namespace='e_contact')),`.
* Implement template `e_contact/contact.html` which can render the
  contact form and submit to `{% url 'e_contact:create' %}`.
* Implement template `e_contact/contact_created.html` to tell the user
  what happens after the form submission.

## Support

This package exists to support my own commercial activities.  Just maybe it can
provide other developers with a helpful hint, or even more.  Feel free to open
Github issues for suggestions or suspected problems, but please don't expect me
to volunteer any time to respond or otherwise address them directly.  Think of
Github issues for this project as a way to document something you'd like me to
be aware of when fixing problems or implementing future requirements.
