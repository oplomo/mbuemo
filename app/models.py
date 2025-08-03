# app/models.py

from django.db import models
from django.utils import timezone

class DisasterReport(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    reported_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Report at ({self.latitude}, {self.longitude}) on {self.reported_at}"
