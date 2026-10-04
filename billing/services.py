from decimal import Decimal, ROUND_HALF_UP


def round_money(value):
    return Decimal(str(value)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


def calculate_tariff_cost(consumption_kwh, tariff):
    if consumption_kwh < 0:
        raise ValueError('Consumption cannot be negative.')
    if tariff is None:
        raise ValueError('A tariff must be provided.')

    total = Decimal('0')
    consumption = Decimal(str(consumption_kwh))
    for tier in tariff.tariff_tiers.order_by('minimum_kwh'):
        lower = Decimal(str(tier.minimum_kwh))
        upper = None if tier.maximum_kwh is None else Decimal(str(tier.maximum_kwh))
        if consumption <= lower:
            continue
        if upper is None:
            chargeable = consumption - lower
        else:
            chargeable = min(consumption, upper) - lower
        if chargeable <= 0:
            continue
        total += chargeable * Decimal(str(tier.rate_per_kwh))
    return round_money(total)


def get_active_tariff(tariffs, on_date=None):
    if not tariffs:
        return None
    active = [tariff for tariff in tariffs if tariff.effective_from <= on_date]
    if not active:
        return tariffs.order_by('-effective_from').first()
    return sorted(active, key=lambda tariff: tariff.effective_from, reverse=True)[0]
