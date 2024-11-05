from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from .models import Recado
from .serializers import RecadoSerializer
from drf_yasg.utils import swagger_auto_schema
import boto3
import os
import uuid

class RecadoView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: RecadoSerializer(many=True)},
        security=[{'Bearer': []}]
    )
    def get(self, request):
        user = request.user
        conta = user.conta
        dispositivo = conta.device_id

        recados = Recado.objects.filter(device_id=dispositivo)
        serializer = RecadoSerializer(recados, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=RecadoSerializer,
        security=[{'Bearer': []}]
    )
    def post(self, request):
        user = request.user
        conta = user.conta
        dispositivo = conta.device_id

        serializer = RecadoSerializer(data=request.data)
        if serializer.is_valid():
            recado = serializer.save(device_id=dispositivo, account_id=conta)
            
            audio_url = self.text_to_speech(recado.message)
            if audio_url:
                recado.audio_url = audio_url
                recado.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def text_to_speech(self, message):
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
            s3_client.upload_file(temp_audio_path, s3_bucket, audio_file_name)
            
            audio_url = f"https://{s3_bucket}.s3.amazonaws.com/{audio_file_name}"

            os.remove(temp_audio_path)
            
            return audio_url

        except Exception as e:
            print(f"Erro ao gerar ou enviar o áudio para o S3: {e}")
            return None