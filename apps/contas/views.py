from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User 
from apps.dispositivos.models import Dispositivo
from apps.contas.models import Conta

from .serializers import ContaCreateSerializer, AlterarSenhaSerializer, ContaListSerializer

class ContaCreateView(APIView):
    @swagger_auto_schema(
        request_body=ContaCreateSerializer,
        # security=[{'Bearer': []}]  # Specify the security requirement
    )
    def post(self, request, *args, **kwargs):
        serializer = ContaCreateSerializer(data=request.data)
        if serializer.is_valid():
            conta = serializer.save()
            return Response({"message": "Conta created successfully.", "conta_id": conta.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AlterarSenhaView(APIView):
    @swagger_auto_schema(
        request_body=AlterarSenhaSerializer,
        # security=[{'Bearer': []}]  # Specify the security requirement
    )
    def post(self, request, *args, **kwargs):
        serializer = AlterarSenhaSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            device_code = serializer.validated_data['device_code']

            user = get_object_or_404(User, email=email)
            conta = get_object_or_404(Conta, user=user.id)
            device = get_object_or_404(Dispositivo, device_code=device_code)

            if user and device and device.id == conta.device_id.id:
                # Save password update
                serializer.update(user, serializer.validated_data)
                return Response({"message": "Password updated successfully.", "account_id": user.id}, 
                                status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ContaListView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: ContaListSerializer(many=True)},
        security=[{'Bearer': []}]  # Specify the security requirement
    )
    def get(self, request):
        contas = Conta.objects.all()
        if request.user.is_superuser:
            contas = Conta.objects.all()
        else:
            contas = Conta.objects.filter(user=request.user)

        serializer = ContaListSerializer(contas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
