from django.contrib.auth.models import User
from rest_framework import serializers
from apps.contas.models import Conta
from apps.dispositivos.models import Dispositivo
from django.contrib.auth import authenticate
from rest_framework.generics import get_object_or_404
from rest_framework.validators import UniqueValidator

class ContaCreateSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())],
        required=True
    )
    device_code = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"error": "Passwords do not match."})
        return data

    def create(self, validated_data):
        # Create User
        try:
            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password']
            )
        except Exception as e:
            raise serializers.ValidationError({"error": f"{e}"})

        # Get Dispositivo with device_code
        get_object_or_404(Dispositivo, device_code=validated_data["device_code"])

        # Create Conta
        conta = Conta.objects.create(
            user=user,
            device_id=Dispositivo.objects.get(device_code=validated_data["device_code"]),
            user_type="1" 
        )

        return conta

class AlterarSenhaSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    device_code = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"error": "Passwords do not match."})
        return data

    def update(self, instance, validated_data):
        instance.set_password(validated_data.get('password'))
        instance.save()
        if authenticate(username=instance.username, password=validated_data.get('password')):
            return instance
        else:
            raise serializers.ValidationError("Password reset failed.")

class ContaListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.CharField(source="user.email", read_only=True)
    device_code = serializers.CharField(source="device_id.device_code", read_only=True)

    class Meta:
        model = Conta
        fields = ['user', 'username', 'email', 'device_id', 'device_code']

    
