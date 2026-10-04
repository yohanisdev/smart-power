from decimal import Decimal

from appliances.models import Appliance
from electricity.models import MeterReading
from insights.models import Insight


def build_insights_for_home(home):
    if home is None:
        return []

    existing = Insight.objects.filter(home=home)
    existing.delete()

    appliance_total = sum((appliance.estimated_kwh() for appliance in Appliance.objects.filter(home=home, is_active=True)), Decimal('0'))
    readings = list(MeterReading.objects.filter(home=home).order_by('reading_date'))
    actual_total = Decimal('0')
    previous = None
    for reading in readings:
        if previous is not None and reading.reading_value_kwh >= previous.reading_value_kwh:
            actual_total += reading.reading_value_kwh - previous.reading_value_kwh
        previous = reading

    created = []
    if appliance_total > Decimal('200'):
        created.append(Insight(home=home, type='high_usage', title='High estimated appliance load', message='The estimated appliance usage is high relative to the home average. Review heavy-duty devices and reduce active hours where possible.', severity='high'))
    if actual_total > Decimal('0') and appliance_total > Decimal('0') and actual_total > appliance_total * Decimal('1.2'):
        created.append(Insight(home=home, type='unusual_usage', title='Actual usage above estimate', message='Actual household consumption is noticeably above the estimate for your appliances. Check recent usage patterns and meter entries for unusual spikes.', severity='medium'))

    highest_appliance = Appliance.objects.filter(home=home, is_active=True).order_by('-power_watts').first()
    if highest_appliance and highest_appliance.power_watts > 1500:
        created.append(Insight(home=home, type='high_power', title='High-power appliance detected', message=f'{highest_appliance.name} is a high-power device; consider using it more efficiently if it runs for long periods.', severity='medium'))

    for insight in created:
        insight.save()
    return created
