from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from apps.historico.urls import router as historico_router
from apps.recados.urls import router as recados_router

router = routers.DefaultRouter()
router.registry.extend(historico_router.registry)
router.registry.extend(recados_router.registry)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('', include('apps.controle_portao.urls')),
]