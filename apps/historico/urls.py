from django.urls import path
from .views import HistoricoListView

urlpatterns = [
    path('historico/', HistoricoListView.as_view(), name='historico-list'),
]
