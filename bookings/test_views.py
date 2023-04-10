from django.test import TestCase
from bookings.models import ContactMessage, Booking, SessionsIndividual
from django.urls import reverse
from django.contrib.auth.models import User # Required to assign User as a borrower


# Views testing
class TestViews(TestCase):

    def test_get_main_page(self):
        """
        Test if main page is loaded correctly and from desired template
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/sessions_list.html')

    def test_get_contact_page(self):
        """
        Test if contact page is loaded correctly and from desired template
        """
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/contact.html')

    # setUp and login required tests based on
    # https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing#how_to_run_the_tests
    def setUp(self):
        # Create a user
        test_user1 = User.objects.create_user(username='testuser1', password='testuser1password')
        test_user1.save()

        # Create an available booking
        test_booking = SessionsIndividual.objects.create(
                day='Tuesday',
                time='10:30',
                booked=False
            )

    def test_redirect_from_booking_if_not_logged_in(self):
        response = self.client.get('/bookings_list/')
        self.assertRedirects(response, '/accounts/login/?/accounts/login=/bookings_list/')

    def test_get_bookings_list_if_logged_in(self):
        """
        Test if bookings page is loaded correctly and from desired template
        """
        login = self.client.login(username='testuser1', password='testuser1password')
        response = self.client.get('/bookings_list/')

        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/bookings_list.html')

    # Work In Progress
    # def test_get_confirm_booking_page(self):
    #     """
    #     Test if confirm_booking page is loaded correctly and from desired
    #     template
    #     """
    #     login = self.client.login(username='testuser1', password='testuser1password')

    #     test_booking = SessionsIndividual.objects.create(
    #             day='Tuesday',
    #             time='10:30',
    #             booked=False
    #         )
    #     response = self.client.post('/bookings_list/', {
    #         'session': test_booking,
    #         'name': 'testuser1',
    #         'address_line_1': 'somewhere',
    #         'address_line_2': '',
    #         'postcode': 'sometown',
    #         'country': 'IE',
    #         'phone': '01234'
    #         })

    #     self.assertEqual(str(response.context['user']), 'testuser1')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'bookings/confirm_booking.html')

    # def test_can_contact(self):
    #     """
    #     Test if contact message can be sent and user redirected correctly
    #     """
    #     response = self.client.post('/contact', {
    #         'name': 'Guest',
    #         'email': 'email@email.com',
    #         'message': 'message'
    #     })
    #     print(response)
    #     self.assertRedirects(response, '/contact/')
