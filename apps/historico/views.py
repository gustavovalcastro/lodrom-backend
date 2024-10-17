from rest_framework import viewsets
from apps.historico.serializers import HistoricoSerializer
from apps.historico.models import Historico

class HistoricoViewSet(viewsets.ModelViewSet):
    queryset = Historico.objects.all()
    serializer_class = HistoricoSerializer
