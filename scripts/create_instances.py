from django.contrib.auth.models import User
from apps.dispositivos.models import Dispositivo
from apps.contas.models import Conta
import dotenv
import os

dotenv.load_dotenv()

def create():
    if not User.objects.filter(is_superuser=True).exists():
        User.objects.create_superuser(
            username=str(os.getenv('SUPERUSER_USERNAME')),
            email=str(os.getenv('SUPERUSER_EMAIL')),
            password=str(os.getenv('SUPERUSER_PASSWORD')),
            is_active=True,
            is_staff=True,
        )

    # Create other important instances
    if not Dispositivo.objects.exists():
        username = str(os.getenv('DEFAULT_DISPOSITIVO_USERNAME'))
        user = User.objects.filter(username=username).first()

        if not user:
            user = User.objects.create_user(
                username=username,
                password=str(os.getenv('DEFAULT_DISPOSITIVO_PASSWORD')),
            )

        Dispositivo.objects.create(
            user=user,
            device_code=str(os.getenv('DEFAULT_DISPOSITIVO_CODE')),
        )

    if not Conta.objects.exists():
        usernames = [
            str(os.getenv('DEFAULT_CONTA_USERNAME')),
            str(os.getenv('DEFAULT_CONTA_USERNAME_2')),
            str(os.getenv('DEFAULT_CONTA_USERNAME_3')),
        ]
        emails = [
            str(os.getenv('DEFAULT_CONTA_EMAIL')),
            str(os.getenv('DEFAULT_CONTA_EMAIL_2')),
            str(os.getenv('DEFAULT_CONTA_EMAIL_3')),
        ]
        phone_numbers = [
            str(os.getenv('DEFAULT_CONTA_PHONE')),
            str(os.getenv('DEFAULT_CONTA_PHONE_2')),
            str(os.getenv('DEFAULT_CONTA_PHONE_3')),
        ]
        for i, username in enumerate(usernames):
            user = User.objects.filter(username=username).first()

            if not user:
                user = User.objects.create_user(
                    username=username,
                    email=emails[i],
                    password=str(os.getenv('DEFAULT_CONTA_PASSWORD')),
                )

                device = Dispositivo.objects.filter(device_code=str(os.getenv('DEFAULT_DISPOSITIVO_CODE'))).first()
                Conta.objects.create(
                    user=user,
                    device_id=device,
                    phone_number=phone_numbers[i],
                )
