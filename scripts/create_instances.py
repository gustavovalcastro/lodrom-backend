from asyncio import Event
from django.core.checks import messages
from django.utils.duration import datetime
import dotenv
import os

from django.contrib.auth.models import User
from apps.dispositivos.models import Dispositivo
from apps.contas.models import Conta
from apps.recados.models import Recado
from apps.historico.models import Historico

dotenv.load_dotenv()

def create():
    if not User.objects.filter(is_superuser=True).exists():
        # Create superuser
        User.objects.create_superuser(username=str(os.getenv('SUPERUSER_USERNAME')), email=str(os.getenv('SUPERUSER_EMAIL')), password=str(os.getenv('SUPERUSER_PASSWORD')), is_active=True, is_staff=True)

        # Create device
        user_d = User.objects.create_user(username=str(os.getenv('DEFAULT_DISPOSITIVO_USERNAME')), password=str(os.getenv('DEFAULT_DISPOSITIVO_PASSWORD')))
        dispositivo = Dispositivo.objects.create(user=user_d, device_code=str(os.getenv('DEFAULT_DISPOSITIVO_CODE')))

        # Create users
        for i in range(3):
            user_conta = User.objects.create_user(username=str(os.getenv(f'DEFAULT_CONTA_USERNAME_{i+1}')), email=os.getenv(f'DEFAULT_CONTA_EMAIL_{i+1}'), password=str(os.getenv('DEFAULT_CONTA_PASSWORD')))
            Conta.objects.create(user=user_conta, device_id=dispositivo, phone_number=str(os.getenv(f'DEFAULT_CONTA_PHONE_{i+1}')))

        # Create historico
        device = Dispositivo.objects.get(id=1)

        account_1 = Conta.objects.get(id=1)
        account_2 = Conta.objects.get(id=2)
        account_3 = Conta.objects.get(id=3)

        Historico.objects.create(device_id=device, event_time="2024-11-04 14:30:00-03:00", event_type="1")
        Historico.objects.create(device_id=device, event_time="2024-11-04 15:30:30-03:00", event_type="3")
        Historico.objects.create(device_id=device, event_time="2024-11-04 15:31:03-03:00", event_type="4")
        Historico.objects.create(device_id=device, event_time="2024-11-04 15:31:03-03:00", event_type="2", account_id=account_1)
        Historico.objects.create(device_id=device, event_time="2024-11-04 19:53:03-03:00", event_type="3")
        Historico.objects.create(device_id=device, event_time="2024-11-04 19:53:45-03:00", event_type="4")
        Historico.objects.create(device_id=device, event_time="2024-11-04 20:50:03-03:00", event_type="2", account_id=account_2)
        Historico.objects.create(device_id=device, event_time="2024-11-04 21:51:01-03:00", event_type="1")
        Historico.objects.create(device_id=device, event_time="2024-11-04 21:52:01-03:00", event_type="5")
        Historico.objects.create(device_id=device, event_time="2024-11-04 22:45:30-03:00", event_type="2", account_id=account_3)

        # create recados
        Recado.objects.create(device_id=device, account_id=account_1, message="Olá! Aguarde um instante para ser atendido.")
        Recado.objects.create(device_id=device, account_id=account_3, message="Se deseja entregar encomendas, entregue-as no apartamento 101.")
        Recado.objects.create(device_id=device, account_id=account_1, message="Estarei disponível a partir das 17h.", start_time="08:00:00", end_time="17:00:00")
        Recado.objects.create(device_id=device, account_id=account_2, message="Estou disponível de segunda a sexta. Volte outra hora.", days_week=["sun", "sat"])
        Recado.objects.create(device_id=device, account_id=account_2, message="Aguarde mais um pouco, pois posso estar descendo as escadas.")
        Recado.objects.create(device_id=device, account_id=account_3, message="Se precisa de nós, encaminhe um email para lodrom@lodrom.com.")
        Recado.objects.create(device_id=device, account_id=account_2, message="Se precisa me encontrar, estou na loja ao lado.", start_time="19:00:00", days_week=["tue"])
