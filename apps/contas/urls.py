from django.urls import path
from .views import ContaCreateView, UnloggedChangePasswordView, ContaListView

urlpatterns = [
    path('contas/create/', ContaCreateView.as_view(), name='conta-create'),
    path('contas/reset_password/', UnloggedChangePasswordView.as_view(), name='conta-reset-password-unlogged'),
    path('contas/', ContaListView.as_view(), name='conta-list'),
]
