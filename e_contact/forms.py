try:
    from captcha.fields import ReCaptchaField
    have_recaptcha = True
except ImportError:
    have_recaptcha = False

from django.conf import settings
from django import forms

from .models import Contact


DEFAULT_CONTACT_SETTINGS = {
    'test-non-field-error': False,
    'recaptcha-theme': 'clean',
    'recaptcha-public-key': None,  # i.e., don't use recaptcha!
    'recaptcha-private-key': None,
}


class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ('name', 'email', 'message',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.contact_settings = DEFAULT_CONTACT_SETTINGS.copy()
        if have_recaptcha:
            if hasattr(settings, 'CONTACT_SETTINGS'):
                self.contact_settings.update(settings.CONTACT_SETTINGS)
            if self.contact_settings['recaptcha-public-key']:
                self.fields['captcha'] = ReCaptchaField(
                    attrs={
                        'theme': self.contact_settings['recaptcha-theme'],
                    },
                    public_key=self.contact_settings['recaptcha-public-key'],
                    private_key=self.contact_settings['recaptcha-private-key'],
                )

    def clean(self):
        if self.contact_settings['test-non-field-error']:
            raise forms.ValidationError('Non-field-error test')
        super().clean()
