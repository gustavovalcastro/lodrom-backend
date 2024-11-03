from django.db import models
from apps.dispositivos.models import Dispositivo
from apps.contas.models import Conta
from django.core.exceptions import ValidationError

class Portao(models.Model):
    device_id = models.ForeignKey(to=Dispositivo, on_delete=models.CASCADE)
    account_id = models.ForeignKey(to=Conta, on_delete=models.CASCADE)
    pin = models.CharField(max_length=4, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Portoes"

    def __str__(self):
        return f"Portão do {self.account_id.user.username}"

    def save(self, *args, **kwargs):
        # Check if the instance is being updated
        if self.pk is not None:
            original = Portao.objects.get(pk=self.pk)
            if original.account_id != self.account_id:
                raise ValidationError("You can't change the account_id field.")
            if original.device_id != self.device_id:
                raise ValidationError("You can't change the device_id field..")
        super().save(*args, **kwargs)
