from django.test import TestCase
from contact.forms import ContactForm
from contact.models import ContactMessage
from django.urls import reverse
# Required to assign User as a borrower
from django.contrib.auth.models import User


class TestContactForm(TestCase):

    def test_email_is_required(self):
        """
        Test if email is required in contact form
        """
        form = ContactForm({'email': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors.keys())
        self.assertEqual(form.errors['email'][0], 'This field is required.')

    def test_message_is_required(self):
        """
        Test if message is required in contact form
        """
        form = ContactForm({'email': 'gg@gg.com', 'message': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('message', form.errors.keys())
        self.assertEqual(form.errors['message'][0], 'This field is required.')


# Views testing
class TestViews(TestCase):
    def test_get_contact_page(self):
        """
        Test if contact page is loaded correctly and from desired template
        """
        response = self.client.get('/contact_us/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact/contact_us.html')
