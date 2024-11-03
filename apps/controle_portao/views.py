from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .serializers import OpenPortaoSerializer, PortaoListSerializer, ResetPinSerializer, SetPinSerializer
from .models import Portao
from apps.contas.models import Conta

class OpenPortaoView(APIView):
    serializer_class = OpenPortaoSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=OpenPortaoSerializer,
        security=[{'Bearer': []}]  # Specify the security requirement
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            return Response({"message": "Portao has opened successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SetPinView(APIView):
    serializer_class = SetPinSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=SetPinSerializer,
        security=[{'Bearer': []}]  # Specify the security requirement
    )
    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            conta = get_object_or_404(Conta, user=user)
            portao = get_object_or_404(Portao, account_id=conta)

            serializer.update(portao, request.data)
            return Response({"message": "PIN has been set successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPinView(APIView):
    serializer_class = ResetPinSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=ResetPinSerializer,
        security=[{'Bearer': []}]  # Specify the security requirement
    )
    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            conta = get_object_or_404(Conta, user=user)
            portao = get_object_or_404(Portao, account_id=conta)

            serializer.update(portao, request.data)
            return Response({"message": "PIN has been reset successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PortaoListView(APIView):
    serializer_class = PortaoListSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: PortaoListSerializer(many=True)},
        security=[{'Bearer': []}]  # Specify the security requirement
    )
    def get(self, request):
        if request.user.is_superuser:
            portoes = Portao.objects.all()
        else:
            conta = Conta.objects.filter(user=request.user).first()  # Use .first() to get a single instance or None
            if conta is None:
                return Response({"detail": "No account found for the user."}, status=status.HTTP_404_NOT_FOUND)
            portoes = Portao.objects.filter(account_id=conta)  # Use .filter() to get a queryset

        serializer = PortaoListSerializer(portoes, many=True)
        return Response(serializer.data)
