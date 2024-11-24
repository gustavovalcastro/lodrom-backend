from rest_framework import serializers
from apps.recados.models import Recado

class RecadoListSerializer(serializers.ModelSerializer):
    message_id = serializers.IntegerField(source="id", read_only=True)
    username = serializers.CharField(source="account_id.user.username", read_only=True)
    device_code = serializers.CharField(source="device_id.device_code", read_only=True)

    class Meta:
        model = Recado
        fields = ['message_id', 'username', 'device_code',  'message',  'created_at', 'start_time', 'end_time', 'days_week']

class RecadoCreateSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=200)
    created_at = serializers.DateTimeField(read_only=True)
    start_time = serializers.TimeField(required=False)
    end_time = serializers.TimeField(required=False)
    days_week = serializers.ListField(
        child=serializers.ChoiceField(choices=["sun", "mon", "tue", "wed", "thu", "fri", "sat"]),
        required=False,
    )

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

class RecadoEditSerializer(serializers.ModelSerializer):
    message = serializers.CharField(max_length=200)
    created_at = serializers.DateTimeField(read_only=True)
    # start_time = serializers.TimeField(required=False)
    # end_time = serializers.TimeField(required=False)
    start_time = serializers.TimeField(required=False, allow_null=True)
    end_time = serializers.TimeField(required=False, allow_null=True)
    days_week = serializers.ListField(
        child=serializers.ChoiceField(choices=["sun", "mon", "tue", "wed", "thu", "fri", "sat"]),
        required=False,
    )

    class Meta:
        model = Recado
        fields = [ 'message',  'created_at', 'start_time', 'end_time', 'days_week']

    def validate(self, data):
        message_id = self.context['id']

        try:
            recado = Recado.objects.get(pk=message_id)
        except Recado.DoesNotExist:
            raise serializers.ValidationError({"detail": "Recado not found."})

        start_time = data.get('start_time', recado.start_time)
        end_time = data.get('end_time', recado.end_time)

        if start_time and end_time and start_time >= end_time:
            raise serializers.ValidationError({'end_time': "Must be greater than 'start_time'."})

        return data

    def update(self, instance, validated_data):
        instance.message = validated_data['message']
        instance.start_time = validated_data.get('start_time', instance.start_time)  # Corrected line
        instance.end_time = validated_data.get('end_time', instance.end_time)
        instance.days_week = validated_data.get('days_week', instance.days_week)
        instance.save()
        return instance
