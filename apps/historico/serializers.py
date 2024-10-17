from rest_framework import serializers
from apps.historico.models import Historico

class HistoricoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Historico
        fields = '__all__'
        # exclude = ['event_time']
