from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from appliances.models import Appliance
from homes.models import Home


class ApplianceEstimateTests(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(username='user1', password='pass1234')
        self.home = Home.objects.create(user=user, name='Main Home')

    def test_appliance_estimate_kwh(self):
        appliance = Appliance.objects.create(
            home=self.home,
            name='Heater',
            category='HVAC',
            power_watts=1000,
            average_hours_per_day=1,
            days_per_period=30,
            quantity=1,
        )
        self.assertEqual(appliance.estimated_kwh(), Decimal('30.000'))

    def test_invalid_power_rating_is_rejected(self):
        appliance = Appliance(
            home=self.home,
            name='Bad Device',
            power_watts=-1,
            average_hours_per_day=1,
            days_per_period=30,
        )
        with self.assertRaises(ValidationError):
            appliance.full_clean()
