from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from apps.historico.urls import router as historico_router
from apps.recados.urls import router as recados_router

router = routers.DefaultRouter()
router.registry.extend(historico_router.registry)
router.registry.extend(recados_router.registry)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include('apps.controle_portao.urls')),
    path('', include('apps.contas.urls')),
    path('', include('apps.controle_portao.urls')),
]
