from django.urls import path
from apps.controle_portao.views import ResetPinView
from apps.contas.views import LoggedChangePasswordView, AccountDataView, AccountLogoutView

urlpatterns = [
    path('config/controle_portao/reset_pin/', ResetPinView.as_view(), name='reset-pin-portao'),
    path('config/contas/account_data/', AccountDataView.as_view(), name='edit-account-data'),
    path('config/contas/reset_password/', LoggedChangePasswordView.as_view(), name='conta-reset-password-logged'),
    path('config/contas/logout/', AccountLogoutView.as_view(), name='conta-logout'),
]
