from django.db import models
from django.contrib.auth.models import User
from apps.dispositivos.models import Dispositivo

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import apps 

class Conta(models.Model):
    USER_TYPE = [
        ("1", "Conta"),
        ("2", "Dispositivo"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=14, blank=False, null=False)
    device_id = models.ForeignKey(to=Dispositivo, on_delete=models.PROTECT)
    user_type = models.CharField(max_length=1,choices=USER_TYPE,null=False,default="1")

    def __str__(self):
        return self.user.username

@receiver(post_save,sender=Conta)
def create_portao(sender, instance, created, **kwargs):
    if created:
        # print(f"INSTANCE: {instance.id}")
        Portao = apps.get_model('controle_portao', 'Portao')
        Portao.objects.create(
            device_id=instance.device_id,
            account_id=instance,
            pin=None  # You can customize the default value for 'pin' here
        )
