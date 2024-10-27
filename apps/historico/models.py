from django.db import models
from apps.dispositivos.models import Dispositivo
from apps.contas.models import Conta
from django.utils import timezone  # Import timezone

class Historico(models.Model):
    EVENT_TYPES = [
        ("1","Portão destravado pelo gancho"),
        ("2","Portão aberto remotamente"),
        ("3","Mensagens anunciadas"),
        ("4","Interfone tocou"),
    ]

    device_id = models.ForeignKey(to=Dispositivo, on_delete=models.RESTRICT)
    account_id = models.ForeignKey(to=Conta, on_delete=models.CASCADE, null=True, blank=True)
    event_time = models.DateTimeField(default=timezone.now)  # Set default to now
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES, null=False)
