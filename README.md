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

Add these features:

* E-mail validation (user must click on link to fix state of message in db)

## Integration requirements

* Add `e_contact` to `INSTALLED_APPS`.
* Include the URLs via `url(r'^contact/', include('e_contact.urls', namespace='e_contact')),`.
* Implement template `e_contact/contact.html` which can render the
  contact form and submit to `{% url 'e_contact:create' %}`.
* Implement template `e_contact/contact_created.html` to tell the user
  what happens after the form submission.

## Test template handling of form errors

* Add `CONTACT_SETTINGS` dictionary to `settings`, if it doesn't already exist.
* Set the value for `test-non-field-error` to `True` in that dictionary.

## Enabling Google reCAPTCHA

* Sign up for reCAPTCHA.
* Install the `django-recaptcha` package and add `'captcha'` to `INSTALLED_APPS`.
* Add `CONTACT_SETTINGS` dictionary to `settings`, if it doesn't already exist.
* Set values for `recaptcha-public-key` and `recaptcha-private-key` in that
  dictionary.  On production, those will be the values provided when you signed
  up for reCAPTCHA.  For test environments, those will be the values provided
  by Google for anyone to use during testing.  See
  https://developers.google.com/recaptcha/docs/faq#id-like-to-run-automated-tests-with-recaptcha-v2-what-should-i-do
* Set `settings.NOCAPTCHA = True` so that django-recaptcha renders the modern
  Google "I'm not a robot" reCAPTCHA.
* Optionally set a value for `recaptcha-theme` in that dictionary, using one of
  the values documented by Google.
* In your contact form template, ensure that the `captcha` field and its
  `errors` attribute, if set, is rendered.
  This will happen automatically unless your template lays out the form
  manually.

## Enabling SMS notification via Twilio

* Install the `twilio` package from PyPI.
* Configure values for these keys in `CONTACT_SETTINGS`:  `twilio-account-sid`,
  `twilio-auth-token`, `sms-from` (Twilio-provided phone number), and
  `sms-to` (admin's cell phone number in the same format).  You can also set a
  value for `sms-body` to override the default message.
* Add code in your project to call `e_contact.utils.notify()` at an appropriate
  interval.  This will mark all Contacts submitted since the last call as 
  "notified" and send a single SMS.

## Support

This package exists to support my own commercial activities.  Just maybe it can
provide other developers with a helpful hint, or even more.  Feel free to open
Github issues for suggestions or suspected problems, but please don't expect me
to volunteer any time to respond or otherwise address them directly.  Think of
Github issues for this project as a way to document something you'd like me to
be aware of when fixing problems or implementing future requirements.
