from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from electricity.models import MeterReading
from homes.models import Home


class MeterReadingTests(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(username='meteruser', password='pass1234')
        self.home = Home.objects.create(user=user, name='Reading Home')

    def test_period_consumption_from_previous(self):
        previous = MeterReading.objects.create(home=self.home, reading_value_kwh=100, reading_date='2026-01-01', source='manual')
        current = MeterReading(home=self.home, reading_value_kwh=142, reading_date='2026-01-02', source='manual')
        self.assertEqual(current.period_consumption_from_previous(previous), Decimal('42.000'))

    def test_invalid_lower_reading_is_rejected(self):
        previous = MeterReading(home=self.home, reading_value_kwh=150, reading_date='2026-01-01', source='manual')
        current = MeterReading(home=self.home, reading_value_kwh=100, reading_date='2026-01-02', source='manual')
        with self.assertRaises(ValueError):
            current.period_consumption_from_previous(previous)

    def test_negative_reading_is_rejected(self):
        reading = MeterReading(home=self.home, reading_value_kwh=-1, reading_date='2026-01-03', source='manual')
        with self.assertRaises(ValidationError):
            reading.full_clean()
