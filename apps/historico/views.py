from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Historico
from .serializers import HistoricoSerializer
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

class HistoricoAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: HistoricoSerializer(many=True)},
        security=[{'Bearer': []}]  # Specify the security requirement
    )
    def get(self, request):
        historico = Historico.objects.all()
        serializer = HistoricoSerializer(historico, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # @swagger_auto_schema(
        # request_body=HistoricoSerializer,
        # security=[{'Bearer': []}]  # Specify the security requirement
    # )
    # def post(self, request):
        # serializer = HistoricoSerializer(data=request.data)
        # if serializer.is_valid():
            # serializer.save()
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
