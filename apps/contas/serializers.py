from django.contrib.auth.models import User
from rest_framework import serializers
from apps.contas.models import Conta
from apps.dispositivos.models import Dispositivo

class ContaCreateSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    device_code = serializers.CharField(required=True)

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        # Create User
        try:
            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password']
            )
        except:
            raise serializers.ValidationError("Error while creating new account.")

        # Get Dispositivo with device_code
        try:
            device = Dispositivo.objects.get(device_code=validated_data['device_code'])
        except Dispositivo.DoesNotExist:
            raise serializers.ValidationError("Device with given code does not exist.")

        # Create Conta
        conta = Conta.objects.create(
            user=user,
            device_id=device,
            user_type="1"  # Assuming "1" means 'Conta'
        )

        return conta
