from django.test import TestCase


# Views testing
class TestViews(TestCase):

    def test_get_main_page(self):
        """
        Test if main page is loaded correctly and from desired template
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/home.html')
