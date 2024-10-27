from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Recado
from .serializers import RecadoSerializer
from drf_yasg.utils import swagger_auto_schema

class RecadoView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: RecadoSerializer(many=True)},
        security=[{'Bearer': []}]  # Specify the security requirement
    )
    def get(self, request):
        user = request.user
        conta = user.conta
        dispositivo = conta.device_id

        recados = Recado.objects.all().filter(device_id=dispositivo)
        serializer = RecadoSerializer(recados, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=RecadoSerializer,
        security=[{'Bearer': []}]  # Specify the security requirement
    )
    def post(self, request):
        user = request.user
        
        conta = user.conta
        dispositivo = conta.device_id
        
        # Pass the entire request.data to the serializer
        serializer = RecadoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(device_id=dispositivo, account_id=conta)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
