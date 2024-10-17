from django.db import models
from django.contrib.auth.models import User

class Dispositivo(models.Model):
    USER_TYPE = [
        ("1", "Conta"),
        ("2", "Dispositivo"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    device_code = models.CharField(max_length=8, null=False)
    user_type = models.CharField(max_length=1,choices=USER_TYPE,null=False,default="2")

    def __str__(self):
        return self.device_code
