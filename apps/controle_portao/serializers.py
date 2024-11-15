from django.shortcuts import get_object_or_404
from rest_framework import serializers

from apps.contas.models import Conta
from .models import Portao

class OpenPortaoSerializer(serializers.Serializer):
    pin = serializers.CharField(max_length=4)

    def validate(self, data):
        user = self.context['request'].user
        conta = get_object_or_404(Conta, user=user)
        portao = get_object_or_404(Portao, account_id=conta)

        if not portao.pin:
            raise serializers.ValidationError({"detail": "PIN hasn't been set yet."})
        if portao.pin != data['pin']:
            raise serializers.ValidationError({"detail": "Invalid PIN."})

        return data

class CheckPinSerializer(serializers.Serializer):
    def validate(self, data):
        user = self.context['request'].user
        conta = get_object_or_404(Conta, user=user)
        portao = get_object_or_404(Portao, account_id=conta)

        if not portao.pin:
            raise serializers.ValidationError({"detail": "PIN hasn't been set yet."})

        return data

class SetPinSerializer(serializers.Serializer):
    pin1 = serializers.CharField(max_length=4, min_length=4)
    pin2 = serializers.CharField(max_length=4, min_length=4)

    def validate(self, data):
        user = self.context['request'].user
        conta = get_object_or_404(Conta, user=user)
        portao = get_object_or_404(Portao, account_id=conta)

        if data['pin1'] != data['pin2']:
            raise serializers.ValidationError({"detail": "PINs do not match."})
        if portao.pin:
            raise serializers.ValidationError({"detail": "PIN has already been set."})
        if data['pin1'].isalpha():
            raise serializers.ValidationError({"detail": "PIN must only contain numbers."})

        return data

    def update(self, instance, validated_data):
        instance.pin = validated_data.get('pin1')
        instance.save()

class ResetPinSerializer(serializers.Serializer):
    pin1 = serializers.CharField(max_length=4, min_length=4)
    pin2 = serializers.CharField(max_length=4, min_length=4)

    def validate(self, data):
        user = self.context['request'].user
        conta = get_object_or_404(Conta, user=user)
        portao = get_object_or_404(Portao, account_id=conta)

        if data['pin1'] != data['pin2']:
            raise serializers.ValidationError({"detail": "PINs do not match."})
        if not portao.pin:
            raise serializers.ValidationError({"detail": "PIN hasn't been set yet."})
        if data['pin1'].isalpha():
            raise serializers.ValidationError({"detail": "PIN must only contain numbers."})

        return data

    def update(self, instance, validated_data):
        instance.pin = validated_data.get('pin1')
        instance.save()

class PortaoListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="account_id.user.username", read_only=True)
    device_code = serializers.CharField(source="device_id.device_code", read_only=True)

    class Meta:
        model = Portao
        fields = ['account_id', 'username', 'device_id', 'device_code']
