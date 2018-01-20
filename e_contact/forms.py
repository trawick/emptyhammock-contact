from django.conf import settings
from django import forms

from .models import Contact


class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ('name', 'email', 'message', )

    def clean(self):
        if hasattr(settings, 'CONTACT_SETTINGS'):
            if settings.CONTACT_SETTINGS.get('test-non-field-error'):
                raise forms.ValidationError('Non-field-error test')
        super().clean()
