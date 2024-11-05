from django.db import models
from apps.dispositivos.models import Dispositivo
from apps.contas.models import Conta
from django.utils import timezone
import json
from django.core.exceptions import ValidationError

class Recado(models.Model):
    device_id = models.ForeignKey(to=Dispositivo, on_delete=models.RESTRICT)
    account_id = models.ForeignKey(to=Conta, on_delete=models.CASCADE)
    message = models.CharField(max_length=200, null=False, blank=False)
    audio_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    days_week = models.CharField(max_length=100, null=True, blank=True)  # JSON string
    #path/url

    def clean(self):
        if self.days_week:
            try:
                days = json.loads(self.days_week)
                allowed_days = {"sun", "mon", "tue", "wed", "thu", "fri", "sat"}
                if not all(day in allowed_days for day in days):
                    raise ValidationError("Invalid days in days_week.")
            except json.JSONDecodeError:
                raise ValidationError("days_week must be a valid JSON list.")

    def save(self, *args, **kwargs):
        if isinstance(self.days_week, list):
            self.days_week = json.dumps(self.days_week)
        super().save(*args, **kwargs)
