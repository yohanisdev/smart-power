from datetime import date
from decimal import Decimal

from django.test import TestCase

from billing.models import Tariff, TariffTier
from billing.services import calculate_tariff_cost


class TariffCostTests(TestCase):
    def test_tariff_calculation_matches_tiered_usage(self):
        tariff = Tariff.objects.create(name='Demo Tariff', provider='Demo Provider', effective_from=date(2025, 1, 1))
        TariffTier.objects.create(tariff=tariff, minimum_kwh=0, maximum_kwh=50, rate_per_kwh=1)
        TariffTier.objects.create(tariff=tariff, minimum_kwh=50, maximum_kwh=100, rate_per_kwh=2)
        TariffTier.objects.create(tariff=tariff, minimum_kwh=100, maximum_kwh=None, rate_per_kwh=3)

        cost = calculate_tariff_cost(142, tariff)
        self.assertEqual(cost, Decimal('276.00'))

    def test_negative_consumption_is_rejected(self):
        tariff = Tariff.objects.create(name='Demo Tariff', provider='Demo Provider', effective_from=date(2025, 1, 1))
        with self.assertRaises(ValueError):
            calculate_tariff_cost(-5, tariff)
