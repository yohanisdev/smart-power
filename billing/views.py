from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from billing.models import Tariff
from billing.services import calculate_tariff_cost


@login_required
def billing_overview(request):
    tariffs = Tariff.objects.all()
    sample_consumption = 142
    sample_cost = 0
    if tariffs.exists():
        tariff = tariffs.first()
        sample_cost = calculate_tariff_cost(sample_consumption, tariff)
    return render(request, 'billing/billing_overview.html', {'tariffs': tariffs, 'sample_consumption': sample_consumption, 'sample_cost': sample_cost})
