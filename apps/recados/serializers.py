from rest_framework import serializers
from apps.recados.models import Recado
from datetime import datetime

class RecadoSerializer(serializers.ModelSerializer):
    days_week = serializers.ListField(
        child=serializers.ChoiceField(choices=["sun", "mon", "tue", "wed", "thu", "fri", "sat"]),
        required=False
    )

    class Meta:
        model = Recado
        fields = ['device_id', 'account_id', 'message', 'created_at', 'start_time', 'end_time', 'days_week']
        read_only_fields = ['device_id', 'account_id', 'created_at']

    def validate(self, data):
        start_time = data.get('start_time')
        end_time = data.get('end_time')

        if start_time and end_time:
            if start_time >= end_time:
                raise serializers.ValidationError({'end_time': "Must be greater than 'start_time'."})

        return data


    def create(self, validated_data):
        device_id = validated_data.pop('device_id')
        account_id = validated_data.pop('account_id')
        return Recado.objects.create(device_id=device_id, account_id=account_id, **validated_data)

    def to_representation(self, instance):
        """Directly return days_week as a list."""
        representation = super().to_representation(instance)
        representation['days_week'] = instance.days_week if instance.days_week else []
        return representation

    def to_internal_value(self, data):
        return super().to_internal_value(data)
