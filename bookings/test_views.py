from django.test import TestCase


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

    # Following two tests need user log in
    # def test_get_bookings_list(self):
    #     """
    #     Test if bookings page is loaded correctly and from desired template
    #     """
    #     response = self.client.get('/bookings_list/')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'bookings/bookings_list.html')

    # def test_get_confirm_booking_page(self):
    #     """
    #     Test if confirm_booking page is loaded correctly and from desired
    #     template
    #     """
    #     response = self.client.get('/confirm_booking')
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
