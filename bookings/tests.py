from django.test import TestCase
from bookings.forms import BookingsForm
from bookings.models import SessionsIndividual


# class FirstTest(TestCase):
#     @classmethod
#     def setUp(self):
#         # Set up data for the whole TestCase
#         self.sessions = SessionsIndividual.objects.create(
#             day='Tuesday',
#             time='11:00',
#             booked='True'
#         )

#     def test_get_session_list(self):
#         self.assertEqual(self.sessions.day, 'Tuesday')


class TestViews(TestCase):

    def test_get_sessions_list(self):
        """
        Test if sessions_list view responds as expected
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/sessions_list.html')

    def test_get_contact(self):
        """
        Test if contact view responds as expected
        """
        response = self.client.get('/contact')
        print(response)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/contact.html')
