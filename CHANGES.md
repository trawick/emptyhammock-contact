# Changes and migration requirements

## Version 0.0.3

* Support Google's reCAPTCHA on the contact form.
* Add mechanism for testing template handling of form errors:  Add this setting:
    ```
    CONTACT_SETTINGS = {
        'test-non-field-error': True
    }
    ```
