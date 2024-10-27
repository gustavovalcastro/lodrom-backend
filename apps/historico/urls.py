from django.urls import path
from .views import HistoricoAPIView

urlpatterns = [
    path('historico/', HistoricoAPIView.as_view(), name='historico-api'),
]
