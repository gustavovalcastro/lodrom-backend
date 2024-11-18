from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from .serializers import RecadoEditSerializer, RecadoCreateSerializer, RecadoListSerializer
from drf_yasg.utils import swagger_auto_schema
import boto3
import os
import uuid
from .models import Recado
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
            recado = serializer.save(device_id=dispositivo, account_id=conta)
            
            audio_url = self.text_to_speech(recado.message, dispositivo.device_code)
            if audio_url:
                recado.audio_url = audio_url
                recado.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def text_to_speech(self, message, folder):
        polly_client = boto3.client(
            "polly",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION_NAME
        )
        
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION_NAME
        )

        try:
            response = polly_client.synthesize_speech(
                Text=message,
                OutputFormat="mp3",
                VoiceId="Ricardo" #Camila
            )

            audio_file_name = f"recado_{uuid.uuid4()}.mp3"
            
            temp_audio_path = os.path.join(settings.MEDIA_ROOT, audio_file_name)
            with open(temp_audio_path, 'wb') as audio_file:
                audio_file.write(response['AudioStream'].read())
            
            s3_bucket = settings.AWS_S3_BUCKET_NAME
            s3_key = f"{folder}/{audio_file_name}"
            s3_client.upload_file(temp_audio_path, s3_bucket, s3_key)
            
            audio_url = f"https://{s3_bucket}.s3.amazonaws.com/{s3_key}"

            os.remove(temp_audio_path)
            
            return audio_url

        except Exception as e:
            print(f"Error while creating audio or sending it to S3: {e}")
            return None

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
