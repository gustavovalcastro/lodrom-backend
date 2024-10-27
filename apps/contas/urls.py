from django.urls import path
from .views import ContaCreateView

urlpatterns = [
    path('contas/create/', ContaCreateView.as_view(), name='conta-create'),
]
