from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .serializers import OpenPortaoSerializer, PortaoListSerializer, ResetPinSerializer, \
        CheckPinSerializer, SetPinSerializer
from .models import Portao
from apps.contas.models import Conta
from .mqtt_utils import publish_to_mqtt

class OpenPortaoView(APIView):
    serializer_class = OpenPortaoSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=OpenPortaoSerializer,
        security=[{'Bearer': []}]
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            # Retrieve the authenticated user's device_code
            try:
                user = request.user
                conta = get_object_or_404(Conta, user=user)
                device_code = user=conta.device_id.device_code
            except Exception as e:
                return Response({"error": f"{e}"},
                                status=status.HTTP_400_BAD_REQUEST)

            # MQTT topic and payload
            topic = f"{device_code}/controle_portao"
            payload = {"open": True, "device_code": device_code}

            # Publish to MQTT broker
            try:
                publish_to_mqtt(topic, payload)
                return Response({"message": "Portao has opened successfully."}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": f"Failed to publish to MQTT broker: {str(e)}"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CheckPinView(APIView):
    serializer_class = CheckPinSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: CheckPinSerializer(many=True)},
        security=[{'Bearer': []}]  # Specify the security requirement
    )
    def get(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            return Response({"message": "PIN has already been created."}, status=status.HTTP_200_OK)
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

