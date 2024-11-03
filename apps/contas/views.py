from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.contrib.auth.models import User 
from apps.dispositivos.models import Dispositivo
from apps.contas.models import Conta

from .serializers import ContaCreateSerializer, LoggedChangePasswordSerializer, \
        UnloggedChangePasswordSerializer, ContaListSerializer, AccountDataEditSerializer

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

class LoggedChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=LoggedChangePasswordSerializer,
        security=[{'Bearer': []}]  # Specify the security requirement
    )
    def put(self, request, *args, **kwargs):
        serializer = LoggedChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            serializer.update(user, serializer.validated_data)
            return Response({"message": "Password has been updated successfully.", "account_id": user.id}, 
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UnloggedChangePasswordView(APIView):
    @swagger_auto_schema(
        request_body=UnloggedChangePasswordSerializer,
        # security=[{'Bearer': []}]  # Specify the security requirement
    )
    def put(self, request, *args, **kwargs):
        serializer = UnloggedChangePasswordSerializer(data=request.data)
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

class AccountDataView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: ContaListSerializer(many=True)},
        security=[{'Bearer': []}]  # Specify the security requirement
    )
    def get(self, request):
        conta = Conta.objects.filter(user=request.user)

        serializer = ContaListSerializer(conta, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=AccountDataEditSerializer,
        security=[{'Bearer': []}]  # Specify the security requirement
    )
    def put(self, request, *args, **kwargs):
        serializer = AccountDataEditSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            serializer.update(user, serializer.validated_data)
            return Response({"message": "Account information has been changed successfully.", 
                                "account_id": user.id},
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
        
class AccountLogoutView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
            operation_description="Logout by blacklisting the refresh token",
            request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token to blacklist')
                },
                required=['refresh']
            ),
            responses={
                205: openapi.Response(description="Successfully logged out."),
                400: openapi.Response(description="Token is invalid or expired, or refresh token is missing."),
            }
    )
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"detail": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)
        
        except Exception as e:
            return Response({"detail": "Token is invalid or expired."}, status=status.HTTP_400_BAD_REQUEST)
