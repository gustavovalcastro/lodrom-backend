from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from apps.dispositivos.models import Dispositivo
import boto3

from .serializers import RecadoEditSerializer, RecadoCreateSerializer, RecadoListSerializer
from .audio_utils import AudioUtils
from .mqtt_utils import publish_to_mqtt
from .models import Recado
from apps.contas.models import Conta

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
        security=[{'Bearer': []}]
    )
    def post(self, request):
        user = request.user

        try:
            conta = user.conta
            dispositivo = conta.device_id
        except AttributeError:
            return Response({"error": "User is not associated with a valid account or device."}, 
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = RecadoCreateSerializer(data=request.data)
        if serializer.is_valid():
            # Save the Recado instance
            recado = serializer.save(device_id=dispositivo, account_id=conta)

            # Generate the audio URL
            audio_url = AudioUtils.text_to_speech(recado.message, dispositivo.device_code)
            if audio_url:
                recado.audio_url = audio_url
                recado.save()

                # MQTT publishing
                topic = f"{dispositivo.device_code}/recados"
                payload = {
                    "type": 1,
                    "audio_url": audio_url,
                    "device_id": dispositivo.device_code
                }
                try:
                    publish_to_mqtt(topic, payload)
                except Exception as e:
                    return Response(
                        {"error": f"Failed to publish MQTT message: {str(e)}"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )

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

        old_message = recado.message
        old_audio_url = recado.audio_url

        serializer = RecadoEditSerializer(recado, data=request.data, partial=True, context={'id': pk})
        if serializer.is_valid():
            updated_recado = serializer.save()

            if old_message != updated_recado.message:
                # Delete old audio if the message has changed
                if old_audio_url:
                    AudioUtils.delete_s3_file(old_audio_url)

                # Generate new audio
                audio_url = AudioUtils.text_to_speech(updated_recado.message, updated_recado.device_id.device_code)
                if audio_url:
                    updated_recado.audio_url = audio_url
                    updated_recado.save()

            return Response({"detail": "Recado has been updated successfully.", "message_id": updated_recado.id}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RecadoDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            recado = Recado.objects.get(pk=pk)
        except Recado.DoesNotExist:
            return Response({"detail": "Recado was not found.", "id": pk}, status=status.HTTP_404_NOT_FOUND)

        if recado.audio_url:
            try:
                bucket_name = settings.AWS_S3_BUCKET_NAME
                audio_key = recado.audio_url.split(f"https://{bucket_name}.s3.amazonaws.com/")[-1]
                
                s3_client = boto3.client(
                    "s3",
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                    region_name=settings.AWS_REGION_NAME
                )

                s3_client.delete_object(Bucket=bucket_name, Key=audio_key)

            except Exception as e:
                return Response({"detail": f"Failed to delete audio file: {str(e)}", "id": pk}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        recado.delete()

        return Response({"message": "Recado and associated audio have been deleted successfully.", "message_id": pk}, status=status.HTTP_200_OK)
