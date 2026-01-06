from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

class BackendTests(TestCase):

    User = get_user_model()

    def test_redirect_to_login_without_session(self):
        response = self.client.get(reverse("notes:create_note"))
        self.assertEqual(response.status_code, 302)

    def test_get_api_token(self):

        self.user = self.User.objects.create_user(username='test', password='test')

        data = {"username": "test", "password":"test"}
        response = self.client.post(
            reverse("notes:api_get_token"),
            data
        )

        json_data = response.json()
        self.assertIn('token', json_data)
        self.assertIsNotNone(json_data['token'])

    def test_html_sanitization_of_note_preview(self):

        self.client.login(username='test', password='test')

        data = {"markdown": '<script>alert("test")</script>'}
        response = self.client.post(
            reverse("notes:preview_note"),
            data
        )

        self.assertNotIn('script', response.content.decode())
