from django.conf import settings
from django.db import models


class Insight(models.Model):
    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    home = models.ForeignKey('homes.Home', on_delete=models.CASCADE, related_name='insights')
    type = models.CharField(max_length=50, default='general')
    title = models.CharField(max_length=180)
    message = models.TextField()
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='medium')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.home.name}: {self.title}'
