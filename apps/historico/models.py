from django.db import models
from apps.dispositivos.models import Dispositivo
from apps.contas.models import Conta
from django.utils import timezone  # Import timezone

class Historico(models.Model):
    EVENT_TYPES = [
        ("1","Portão destravado pelo gancho"),
        ("2","Portão destravado remotamente"),
        ("3","Interfone tocou"),
        ("4","Interfone foi atendido"),
        ("5","Recados foram enunciados"),
    ]

    device_id = models.ForeignKey(to=Dispositivo, on_delete=models.RESTRICT)
    account_id = models.ForeignKey(to=Conta, on_delete=models.CASCADE, null=True, blank=True)
    event_time = models.DateTimeField(default=timezone.now)  # Set default to now
    event_type = models.CharField(max_length=2, choices=EVENT_TYPES, null=False)
