from django.urls import path
from .views import AlterarSenhaView, ContaCreateView, ContaListView

urlpatterns = [
    path('contas/create/', ContaCreateView.as_view(), name='conta-create'),
    path('contas/reset_password/', AlterarSenhaView.as_view(), name='conta-reset-password'),
    path('contas/', ContaListView.as_view(), name='conta-list'),
]
