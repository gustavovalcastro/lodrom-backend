from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

from .models import Recado
from .serializers import RecadoCreateSerializer, RecadoEditSerializer, RecadoListSerializer
from apps.contas.models import Conta
from apps.dispositivos.models import Dispositivo

class RecadoListView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: RecadoListSerializer(many=True)},
        security=[{'Bearer': []}]  # Specify the security requirement
    )
    def get(self, request):
        if request.user.is_superuser:
            recados = Recado.objects.all()
        else:
            conta = Conta.objects.filter(user=request.user).first()
            device = Dispositivo.objects.filter(user=conta.device_id.user).first()
            recados = Recado.objects.filter(device_id=device)

        serializer = RecadoListSerializer(recados, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RecadoCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=RecadoCreateSerializer,
        security=[{'Bearer': []}]  # Specify the security requirement
    )
    def post(self, request):
        user = request.user
        
        conta = user.conta
        dispositivo = conta.device_id
        
        # Pass the entire request.data to the serializer
        serializer = RecadoCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(device_id=dispositivo, account_id=conta)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RecadoEditView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=RecadoEditSerializer,
        security=[{'Bearer': []}]
    )
    def put(self, request, pk):
        try:
            recado = Recado.objects.get(pk=pk)
        except Recado.DoesNotExist:
            return Response({"detail": "Recado was not found.", "id": pk}, status=status.HTTP_404_NOT_FOUND)

        serializer = RecadoEditSerializer(recado, data=request.data, partial=True, context={'id': pk})
        if serializer.is_valid():
            updated_recado = serializer.save()
            return Response({"detail": "Recado have been updated successfully.", "message_id": updated_recado.id}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RecadoDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            recado = Recado.objects.get(pk=pk)
        except Recado.DoesNotExist:
            return Response({"detail": "Recado was not found.", "id": pk}, status=status.HTTP_404_NOT_FOUND)

        recado.delete() 
        return Response({"message": "Recado has been deleted successfully.", "message_id": pk}, status=status.HTTP_200_OK)
