from django.contrib.auth.models import User
from rest_framework import serializers
from apps.contas.models import Conta
from apps.dispositivos.models import Dispositivo
from django.contrib.auth import authenticate
from rest_framework.generics import get_object_or_404
from rest_framework.validators import UniqueValidator
from .validators import invalid_phone_number

class ContaCreateSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())],
        required=True
    )
    device_code = serializers.CharField(required=True)
    phone_number = serializers.CharField(
        validators=[UniqueValidator(queryset=Conta.objects.all())],
        required=True
    )
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"detail": "Passwords do not match."})
        
        if invalid_phone_number(data['phone_number']):
            raise serializers.ValidationError({"detail": "Phone number must be in the format: (XX)XXXXX-XXXX."})

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
            raise serializers.ValidationError({"detail": f"{e}"})

        # Get Dispositivo with device_code
        device = get_object_or_404(Dispositivo, device_code=validated_data["device_code"])

        # Create Conta
        conta = Conta.objects.create(
            user=user,
            device_id=device,
            phone_number=validated_data['phone_number'],
            user_type="1" 
        )

        return conta

class UnloggedChangePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    device_code = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"detail": "Passwords do not match."})
        return data

    def update(self, instance, validated_data):
        instance.set_password(validated_data.get('password'))
        instance.save()
        if authenticate(username=instance.username, password=validated_data.get('password')):
            return instance
        else:
            raise serializers.ValidationError({"detail": "Password reset has failed."})

class LoggedChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    new_password2 = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        user = self.context['request'].user
        if not authenticate(username=user.username, password=data['current_password']):
            raise serializers.ValidationError({"detail": "Current password is not valid."})
        if data['new_password'] != data['new_password2']:
            raise serializers.ValidationError({"detail": "New passwords do not match."})
        return data

    def update(self, instance, validated_data):
        instance.set_password(validated_data.get('new_password'))
        instance.save()
        if authenticate(username=instance.username, password=validated_data.get('new_password')):
            return instance
        else:
            raise serializers.ValidationError({"detail": "Password reset failed."})

class AccountDataEditSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    phone_number = serializers.CharField(required=True)

    def validate(self, data):
        user = self.context['request'].user
        conta = Conta.objects.filter(user=user).first()

        if invalid_phone_number(data['phone_number']):
            raise serializers.ValidationError({"detail": "Phone number must be in the format: (XX)XXXXX-XXXX."})

        if data['username'] != user.username:
            if User.objects.filter(username=data['username']).exclude(id=user.id).exists():
                raise serializers.ValidationError({"detail": "Username is already taken."})

        if data['email'] != user.email:
            if User.objects.filter(email=data['email']).exclude(id=user.id).exists():
                raise serializers.ValidationError({"detail": "Email is already taken."})

        if conta and data['phone_number'] != conta.phone_number:
            if Conta.objects.filter(phone_number=data['phone_number']).exclude(user=user).exists():
                raise serializers.ValidationError({"detail": "Phone number is already associated with another account."})

        return data

    def update(self, instance, validated_data):
        if instance.username != validated_data.get('username'):
            instance.username = validated_data.get('username')
        if instance.email != validated_data.get('email'):
            instance.email = validated_data.get('email')

        conta = Conta.objects.filter(user=instance.id).first()
        if conta:
            if conta.phone_number != validated_data.get('phone_number'):
                conta.phone_number = validated_data.get('phone_number')
            conta.save()

        instance.save()

class ContaListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.CharField(source="user.email", read_only=True)
    device_code = serializers.CharField(source="device_id.device_code", read_only=True)

    class Meta:
        model = Conta
        fields = ['user', 'username', 'email', 'phone_number', 'device_id', 'device_code']
