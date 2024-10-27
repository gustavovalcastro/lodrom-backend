from rest_framework import serializers
from .models import Historico

class HistoricoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Historico
        fields = ['id', 'device_id', 'account_id', 'event_time', 'event_type']
