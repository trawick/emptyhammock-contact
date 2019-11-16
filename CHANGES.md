# Changes and migration requirements

## Version 0.0.8

* Fix incompatibilities with Python 3.5.

## Version 0.0.7

* Add e-mail as a contact mechanism.
* Add e_contact_notify management command to notify if there are new contact
  requests.

## Version 0.0.6

* Support Django 2.2.

## Version 0.0.5

* The admin can optionally be notified of submitted contact requests via
  Twilio (SMS).
* Contact's `state` field is now editable in admin.

## Version 0.0.4

* Fix show-stopper bug in reCAPTCHA support.

## Version 0.0.3

* Support Google's reCAPTCHA on the contact form.
* Add mechanism for testing template handling of form errors.
