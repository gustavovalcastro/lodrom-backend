import boto3
import os
import uuid
from django.conf import settings
import wave

def pcm_to_wav(pcm_file, wav_file, sample_rate=44100, channels=1, sample_width=2):
    """
    Convert a PCM file to WAV format.

    Args:
        pcm_file (str): Path to the input PCM file.
        wav_file (str): Path to the output WAV file.
        sample_rate (int): The sample rate (e.g., 44100 for 44.1kHz audio).
        channels (int): The number of audio channels (1 for mono, 2 for stereo).
        sample_width (int): Sample width in bytes (2 for 16-bit audio).
    """
    with open(pcm_file, 'rb') as pcm:
        pcm_data = pcm.read()

    with wave.open(wav_file, 'wb') as wav:
        wav.setnchannels(channels)
        wav.setsampwidth(sample_width)
        wav.setframerate(sample_rate)
        wav.writeframes(pcm_data)

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
                OutputFormat="pcm", # wp3
                VoiceId="Ricardo"  # Use desired voice
            )


            audio_file_name = f"recado_{uuid.uuid4()}"
            audio_file_name_pcm = f"{audio_file_name}.pcm"

            temp_audio_path = os.path.join(settings.MEDIA_ROOT, audio_file_name_pcm)

            with open(temp_audio_path, 'wb') as audio_file:
                audio_file.write(response['AudioStream'].read())

            audio_file_name_wav = f"{audio_file_name}.wav"
            temp_output_path = os.path.join(settings.MEDIA_ROOT, audio_file_name_wav)

            # Example usage
            pcm_to_wav(temp_audio_path, temp_output_path, sample_rate=16000, channels=1, sample_width=2)
            
            s3_bucket = settings.AWS_S3_BUCKET_NAME
            s3_key = f"{folder}/{audio_file_name_wav}"
            s3_client.upload_file(temp_output_path, s3_bucket, s3_key)

            audio_url = f"https://{s3_bucket}.s3.amazonaws.com/{s3_key}"
            os.remove(temp_audio_path)
            os.remove(temp_output_path)
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
