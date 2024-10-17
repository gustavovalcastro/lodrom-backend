from rest_framework import serializers
from apps.recados.models import Recado

class RecadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recado
        fields = '__all__'
