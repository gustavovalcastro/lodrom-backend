from rest_framework import serializers
from .models import Historico

class HistoricoSerializer(serializers.ModelSerializer):
    account_username = serializers.CharField(source='account_id.user.username', read_only=True)
    event_description = serializers.SerializerMethodField()

    class Meta:
        model = Historico
        fields = ['id', 'account_id', 'account_username', 'event_time', 'event_type', 'event_description']

    def get_event_description(self, obj):
        descriptions = dict(Historico.EVENT_TYPES)
        return descriptions.get(obj.event_type, "Unknown event")
