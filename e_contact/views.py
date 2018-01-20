from django.shortcuts import reverse
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

from .forms import ContactForm
from .models import Contact


class ContactView(CreateView):
    model = Contact
    form_class = ContactForm

    def get_template_names(self):
        return ['e_contact/contact.html']

    def get_success_url(self):
        return reverse('e_contact:created')


class ContactCreated(TemplateView):
    template_name = 'e_contact/contact_created.html'
