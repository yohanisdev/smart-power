from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from analytics.services import actual_household_usage, appliance_breakdown, daily_usage, estimate_appliance_usage
from insights.services import build_insights_for_home


@login_required
def dashboard_view(request):
    home = request.user.homes.first()
    if not home:
        return render(request, 'dashboard.html', {'home': None, 'actual_usage': 0, 'estimated_usage': 0, 'breakdown': [], 'daily_labels': [], 'daily_values': [], 'breakdown_names': [], 'breakdown_values': []})
    build_insights_for_home(home)
    actual_usage = actual_household_usage(home)
    estimated_usage = estimate_appliance_usage(home)
    breakdown = appliance_breakdown(home)
    daily = daily_usage(home)
    context = {
        'home': home,
        'actual_usage': float(actual_usage),
        'estimated_usage': float(estimated_usage),
        'breakdown': breakdown,
        'daily_labels': list(daily.keys()),
        'daily_values': [float(value) for value in daily.values()],
        'breakdown_names': [item['name'] for item in breakdown],
        'breakdown_values': [float(item['estimated_kwh']) for item in breakdown],
    }
    return render(request, 'dashboard.html', context)


@login_required
def analytics_view(request):
    home = request.user.homes.first()
    context = {'home': home}
    if home:
        context['actual_usage'] = float(actual_household_usage(home))
        context['estimated_usage'] = float(estimate_appliance_usage(home))
        context['breakdown'] = appliance_breakdown(home)
        context['daily'] = daily_usage(home)
    return render(request, 'analytics/analytics_overview.html', context)
