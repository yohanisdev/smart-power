from django.contrib.auth import get_user_model
from django.test import TestCase


class AuthApiTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='apiuser', password='pass1234')

    def test_registration_endpoint(self):
        response = self.client.post('/api/auth/register/', {'username': 'newuser', 'email': 'new@example.com', 'password': 'securePass123!'}, follow=True)
        self.assertEqual(response.status_code, 201)

    def test_protected_home_list_requires_auth(self):
        response = self.client.get('/api/homes/')
        self.assertEqual(response.status_code, 403)

    def test_authenticated_user_can_access_home_list(self):
        self.client.login(username='apiuser', password='pass1234')
        response = self.client.get('/api/homes/')
        self.assertEqual(response.status_code, 200)
