from django.test import TestCase
from bookings.forms import ContactForm, BookingsForm
from bookings.models import ContactMessage, Booking, SessionsIndividual


# Forms testing
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


class BookingForm(TestCase):

    def test_postcode_is_required(self):
        """
        Test if postcode is required in contact form
        """
        form = BookingsForm({'postcode': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('postcode', form.errors.keys())
        self.assertEqual(form.errors['postcode'][0], 'This field is required.')

    def test_address_line_2_is_not_required(self):
        """
        Test if address_line_2 is required in contact form
        """
        session = SessionsIndividual.objects.create(
            day='Tuesday',
            time='10:30',
            booked=False
        )
        form = BookingsForm({
            'session': session,
            'name': 'someone',
            'address_line_1': 'somewhere',
            'address_line_2': '',
            'postcode': 'sometown',
            'country': 'IE',
            'phone': '01234'
            })
        self.assertTrue(form.is_valid())

    def test_session_from_booked_equal_true(self):
        """
        Test if only unbooked sessions are offered for booking
        (SessionsIndividual.booked=False)
        """
        session = SessionsIndividual.objects.create(
            day='Tuesday',
            time='10:30',
            booked=True
        )
        form = BookingsForm({'session': session})
        self.assertFalse(form.is_valid())
        self.assertIn('session', form.errors.keys())
        self.assertEqual(form.errors['session'][0], 'Select a valid choice.'
                         ' That choice is not one of the available choices.')
