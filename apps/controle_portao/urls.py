from django.urls import path
from .views import OpenPortaoView, SetPinView, PortaoListView, CheckPinView

urlpatterns = [
    path('controle_portao/open/', OpenPortaoView.as_view(), name='open-portao'),
    path('controle_portao/check_pin/', CheckPinView.as_view(), name='check-pin-portao'),
    path('controle_portao/set_pin/', SetPinView.as_view(), name='set-pin-portao'),
    path('controle_portao/list/', PortaoListView.as_view(), name='list-portao'),
]
