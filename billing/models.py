from django.core.exceptions import ValidationError
from django.db import models


class Tariff(models.Model):
    name = models.CharField(max_length=120)
    provider = models.CharField(max_length=120, blank=True)
    effective_from = models.DateField()
    effective_to = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-effective_from']

    def __str__(self):
        return self.name

    def clean(self):
        if self.effective_to and self.effective_from > self.effective_to:
            raise ValidationError({'effective_to': 'Effective end date must be after the start date.'})
        super().clean()

    @property
    def tiers(self):
        return self.tariff_tiers.all()


class TariffTier(models.Model):
    tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE, related_name='tariff_tiers')
    minimum_kwh = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    maximum_kwh = models.DecimalField(max_digits=12, decimal_places=3, null=True, blank=True)
    rate_per_kwh = models.DecimalField(max_digits=12, decimal_places=4, default=0)

    class Meta:
        ordering = ['minimum_kwh']

    def __str__(self):
        upper = '∞' if self.maximum_kwh is None else str(self.maximum_kwh)
        return f'{self.tariff.name}: {self.minimum_kwh} kWh - {upper} @ {self.rate_per_kwh}'

    def clean(self):
        if self.minimum_kwh < 0:
            raise ValidationError({'minimum_kwh': 'Minimum usage cannot be negative.'})
        if self.maximum_kwh is not None and self.maximum_kwh < self.minimum_kwh:
            raise ValidationError({'maximum_kwh': 'Maximum usage must be greater than or equal to minimum usage.'})
        if self.rate_per_kwh < 0:
            raise ValidationError({'rate_per_kwh': 'Rate cannot be negative.'})
        super().clean()
