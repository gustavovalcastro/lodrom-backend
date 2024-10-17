from django.urls import path, include
from rest_framework import routers

from apps.historico.views import HistoricoViewSet

router = routers.SimpleRouter()
router.register('historico', HistoricoViewSet, basename='Historico')

# urlpatterns = [
    # path('', include(router.urls)),
# ]
