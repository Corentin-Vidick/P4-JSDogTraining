import unittest
from . import jstraining
from .forms import BookingsForm


class TestBookingsForm(unittest.TestCase):

    def test_postcode_required(self):
        form = BookingsForm({'postcode': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors.keys())


if __name__ == '__main__':
    unittest.main()
