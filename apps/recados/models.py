from django.db import models
from apps.dispositivos.models import Dispositivo
from apps.contas.models import Conta
from django.utils import timezone  # Import timezone

class Recado(models.Model):
    DAYS_WEEK = [
        ("sun", "dom"),
        ("mon", "seg"),
        ("tue", "ter"),
        ("wed", "qua"),
        ("thu", "qui"),
        ("fri", "sex"),
        ("sat", "sab"),
    ]

    device_id = models.ForeignKey(to=Dispositivo, on_delete=models.RESTRICT)
    account_id = models.ForeignKey(to=Conta, on_delete=models.CASCADE)
    message = models.CharField(max_length=200, null=False, blank=False)
    created_at = models.DateTimeField(default=timezone.now)  # Set default to now
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    days_week = models.CharField(max_length=50, choices=DAYS_WEEK, null=True)
