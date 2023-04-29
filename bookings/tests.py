from django.test import TestCase
from django.urls import reverse
# Required to assign User as a borrower
from django.contrib.auth.models import User
from bookings.forms import BookingsForm
from bookings.models import Booking, SessionsIndividual


# Forms testing

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

    def test_session_form_booked_equal_true(self):
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


# Views testing
class TestViews(TestCase):
    # setUp and login required tests based on
    # https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing#how_to_run_the_tests
    def setUp(self):
        # Create a user
        test_user1 = User.objects.create_user(
            username='testuser1', password='testuser1password'
            )
        test_user1.save()

        # Create an available booking
        test_booking = SessionsIndividual.objects.create(
                day='Tuesday',
                time='10:30',
                booked=False
            )

    def test_redirect_from_booking_if_not_logged_in(self):
        response = self.client.get('/bookings_list/')
        self.assertRedirects(
            response, '/accounts/login/?/accounts/login=/bookings_list/'
            )

    def test_get_bookings_list_if_logged_in(self):
        """
        Test if bookings page is loaded correctly and from desired template
        """
        login = self.client.login(
            username='testuser1', password='testuser1password'
            )
        response = self.client.get('/bookings_list/')

        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/bookings_list.html')
