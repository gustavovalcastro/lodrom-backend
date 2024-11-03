from django.urls import path
from .views import OpenPortaoView, SetPinView, PortaoListView

urlpatterns = [
    path('controle_portao/open/', OpenPortaoView.as_view(), name='open-portao'),
    path('controle_portao/set_pin/', SetPinView.as_view(), name='set-pin-portao'),
    path('controle_portao/list/', PortaoListView.as_view(), name='list-portao'),
]
