from unittest import TestCase
from app import app



class FlaskTests(TestCase):

    def setUp(self):
        """Stuff to do before every test."""
        self.client = app.test_client()

    def test_users(self):
        """Make sure users view is available"""

        with self.client:
            response = self.client.get('/users')
            self.assertIn(b'<a href="/users/new" class="btn btn-sm btn-warning"><i class="fas fa-plus-circle"></i>&nbsp;Add user</a>', response.data)
            self.assertIn(b'<div class="table-responsive">', response.data)

    