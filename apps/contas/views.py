from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ContaCreateSerializer

class ContaCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ContaCreateSerializer(data=request.data)
        if serializer.is_valid():
            conta = serializer.save()
            return Response({"message": "Conta created successfully", "conta_id": conta.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
