from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from django.shortcuts import reverse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from .forms import ContactForm
# Create your views here.


class HomeView(TemplateView):
    template_name = 'index.html'


class ContactFormView(FormView):
    form_class = ContactForm
    template_name = 'contact.html'

    def get_success_url(self):
        return reverse('contact')

    def form_valid(self, form):
        messages.info(self.request, "Thanks for contacting us!")
        name = form.cleaned_data.get('name')
        email = form.cleaned_data.get('email')
        message = form.cleaned_data.get('message')

        full_message = f"""
            Received message below from {name}, {email}
            _____________________________


            {message}
            """
        send_mail(
            subject="Received contact form submission",
            message=full_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.NOTIFY_EMAIL]
        )
        return super(ContactForm, self).form_valid(form)
