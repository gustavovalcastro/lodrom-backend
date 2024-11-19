import boto3
import os
import uuid
from django.conf import settings

class AudioUtils:
    @staticmethod
    def text_to_speech(message, folder):
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
                VoiceId="Ricardo"  # Use desired voice
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

    @staticmethod
    def delete_s3_file(audio_url):
        try:
            bucket_name = settings.AWS_S3_BUCKET_NAME
            audio_key = audio_url.split(f"https://{bucket_name}.s3.amazonaws.com/")[-1]
            s3_client = boto3.client(
                "s3",
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION_NAME
            )
            s3_client.delete_object(Bucket=bucket_name, Key=audio_key)
        except Exception as e:
            print(f"Error while deleting S3 file: {e}")
