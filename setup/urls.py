from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

# Swagger API
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

schema_view = get_schema_view(
    openapi.Info(
        title="Lodrom API",
        default_version='v1',
        description="API para back-end do projeto Lodrom",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include('apps.contas.urls')),
    path('', include('apps.historico.urls')),
    path('', include('apps.recados.urls')),
    path('', include('apps.controle_portao.urls')),
    path('', include('apps.config.urls')),
    
    # Swagger API Doc
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# from apps.historico.urls import router as historico_router
# from apps.recados.urls import router as recados_router

# router = routers.DefaultRouter()
# router.registry.extend(historico_router.registry)
# router.registry.extend(recados_router.registry)
