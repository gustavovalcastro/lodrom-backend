from rest_framework import viewsets
from apps.recados.serializers import RecadoSerializer
from apps.recados.models import Recado

class RecadoViewSet(viewsets.ModelViewSet):
    queryset = Recado.objects.all()
    serializer_class = RecadoSerializer
