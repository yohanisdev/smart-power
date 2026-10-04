from collections import defaultdict
from decimal import Decimal

from appliances.models import Appliance
from electricity.models import MeterReading


def estimate_appliance_usage(home):
    return sum(
        (appliance.estimated_kwh() for appliance in Appliance.objects.filter(home=home, is_active=True)),
        Decimal('0'),
    )


def actual_household_usage(home, start_date=None, end_date=None):
    readings = MeterReading.objects.filter(home=home)
    if start_date is not None:
        readings = readings.filter(reading_date__gte=start_date)
    if end_date is not None:
        readings = readings.filter(reading_date__lte=end_date)

    ordered = list(readings.order_by('reading_date'))
    if len(ordered) < 2:
        return Decimal('0')

    total = Decimal('0')
    previous = ordered[0]
    for current in ordered[1:]:
        if current.reading_value_kwh < previous.reading_value_kwh:
            previous = current
            continue
        total += current.reading_value_kwh - previous.reading_value_kwh
        previous = current
    return total


def appliance_breakdown(home):
    rows = []
    for appliance in Appliance.objects.filter(home=home, is_active=True):
        rows.append({
            'id': appliance.id,
            'name': appliance.name,
            'category': appliance.category,
            'estimated_kwh': float(appliance.estimated_kwh()),
        })
    return sorted(rows, key=lambda item: item['estimated_kwh'], reverse=True)


def daily_usage(home, start_date=None, end_date=None):
    readings = MeterReading.objects.filter(home=home)
    if start_date is not None:
        readings = readings.filter(reading_date__gte=start_date)
    if end_date is not None:
        readings = readings.filter(reading_date__lte=end_date)
    by_date = defaultdict(Decimal)
    ordered = readings.order_by('reading_date')
    previous = None
    for reading in ordered:
        if previous is None:
            previous = reading
            continue
        if reading.reading_value_kwh >= previous.reading_value_kwh:
            by_date[reading.reading_date.isoformat()] += reading.reading_value_kwh - previous.reading_value_kwh
        previous = reading
    return dict(sorted(by_date.items()))


def home_summary(home):
    return {
        'actual_usage': float(actual_household_usage(home)),
        'estimated_usage': float(estimate_appliance_usage(home)),
        'appliance_breakdown': appliance_breakdown(home),
    }
