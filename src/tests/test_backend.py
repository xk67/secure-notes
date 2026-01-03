from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

class BackendTests(TestCase):

    User = get_user_model()

    def test_redirect_to_login_without_session(self):
        response = self.client.get(reverse("notes:create_note"))
        self.assertEqual(response.status_code, 302)
