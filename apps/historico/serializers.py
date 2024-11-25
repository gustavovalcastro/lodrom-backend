from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from .models import Historico
from apps.dispositivos.models import Dispositivo
from .telegram import send

class HistoricoSerializer(serializers.ModelSerializer):
    account_username = serializers.CharField(source='account_id.user.username', read_only=True)
    event_description = serializers.SerializerMethodField()

    class Meta:
        model = Historico
        fields = ['id', 'account_id', 'account_username', 'event_time', 'event_type', 'event_description']

    def get_event_description(self, obj):
        descriptions = dict(Historico.EVENT_TYPES)
        return descriptions.get(obj.event_type, "Unknown event")

class HistoricoCreateSerializer(serializers.Serializer):
    device_code = serializers.CharField(max_length=8, required=True)
    event_type = serializers.ChoiceField(choices=Historico.EVENT_TYPES, required=True)

    def create(self, validated_data):
        device_code = validated_data['device_code']
        event_type = validated_data['event_type']

        dispositivo = get_object_or_404(Dispositivo, device_code=device_code)

        # Create the Historico instance
        historico = Historico.objects.create(
            device_id=dispositivo,
            event_type=event_type
        )

        # Call the send function if event_type is "3"
        if event_type == "3":
            send()

        return historico
