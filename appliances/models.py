from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models

from homes.models import Home


class Appliance(models.Model):
    CATEGORY_CHOICES = [
        ('HVAC', 'HVAC'),
        ('Kitchen', 'Kitchen'),
        ('Laundry', 'Laundry'),
        ('Lighting', 'Lighting'),
        ('Electronics', 'Electronics'),
        ('Water Heating', 'Water Heating'),
        ('Other', 'Other'),
    ]

    home = models.ForeignKey(Home, on_delete=models.CASCADE, related_name='appliances')
    name = models.CharField(max_length=120)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='Other')
    power_watts = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    average_hours_per_day = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    days_per_period = models.DecimalField(max_digits=10, decimal_places=2, default=30)
    quantity = models.PositiveIntegerField(default=1)
    standby_power_watts = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.home.name})'

    def clean(self):
        if not self.name or not self.name.strip():
            raise ValidationError({'name': 'Appliance name is required.'})
        if self.power_watts < 0:
            raise ValidationError({'power_watts': 'Power rating cannot be negative.'})
        if self.average_hours_per_day < 0:
            raise ValidationError({'average_hours_per_day': 'Daily operating hours cannot be negative.'})
        if self.days_per_period <= 0:
            raise ValidationError({'days_per_period': 'The period length must be greater than zero.'})
        if self.quantity <= 0:
            raise ValidationError({'quantity': 'Quantity must be greater than zero.'})
        super().clean()

    def estimated_kwh(self):
        watts = Decimal(str(self.power_watts))
        hours = Decimal(str(self.average_hours_per_day))
        days = Decimal(str(self.days_per_period))
        quantity = Decimal(self.quantity)
        return (watts * hours * days * quantity) / Decimal('1000')

    @property
    def estimated_kwh_value(self):
        return float(self.estimated_kwh())
