from django.contrib.auth import get_user_model
from django.test import TestCase

from homes.models import Home


class HomeTests(TestCase):
    def test_home_creation(self):
        user = get_user_model().objects.create_user(username='homeuser', password='pass1234')
        home = Home.objects.create(user=user, name='Family Home', description='A test home')
        self.assertEqual(str(home), 'Family Home')
