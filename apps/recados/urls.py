from django.urls import path
from .views import RecadoView

urlpatterns = [
    path('recados/', RecadoView.as_view(), name='recados'),
]
