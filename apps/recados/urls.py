from django.urls import path, include
from rest_framework import routers

from apps.recados.views import RecadoViewSet

router = routers.SimpleRouter()
router.register('recados', RecadoViewSet, basename='Recados')

# urlpatterns = [
    # path('', include(router.urls)),
# ]
