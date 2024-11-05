from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

from .models import Historico
from .serializers import HistoricoSerializer
from apps.contas.models import Conta

class HistoricoListView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: HistoricoSerializer(many=True)},
        security=[{'Bearer': []}]  # Specify the security requirement
    )
    def get(self, request):
        conta = Conta.objects.get(user=request.user)
        device_id = conta.device_id
        historicos = Historico.objects.filter(device_id=device_id)
        serializer = HistoricoSerializer(historicos, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
