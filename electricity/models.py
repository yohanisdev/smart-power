from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models

from homes.models import Home


class MeterReading(models.Model):
    SOURCE_CHOICES = [
        ('manual', 'Manual'),
        ('csv_import', 'CSV Import'),
        ('smart_meter', 'Smart Meter'),
        ('authorized_utility_api', 'Authorized Utility API'),
    ]

    home = models.ForeignKey(Home, on_delete=models.CASCADE, related_name='meter_readings')
    reading_value_kwh = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    reading_date = models.DateField()
    source = models.CharField(max_length=30, choices=SOURCE_CHOICES, default='manual')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['reading_date']

    def __str__(self):
        return f'{self.home.name}: {self.reading_value_kwh} kWh on {self.reading_date}'

    def clean(self):
        if self.reading_value_kwh < 0:
            raise ValidationError({'reading_value_kwh': 'Reading cannot be negative.'})
        if not self.reading_date:
            raise ValidationError({'reading_date': 'A valid date is required.'})
        super().clean()

    def period_consumption_from_previous(self, previous_reading):
        if previous_reading is None:
            return Decimal('0')
        if self.reading_value_kwh < previous_reading.reading_value_kwh:
            raise ValueError('Current reading is lower than the previous reading; this is not a valid cumulative sequence.')
        return self.reading_value_kwh - previous_reading.reading_value_kwh
