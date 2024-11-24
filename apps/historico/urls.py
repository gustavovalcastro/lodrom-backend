from django.urls import path
from .views import HistoricoListView, HistoricoCreateView

urlpatterns = [
    path('historico/', HistoricoListView.as_view(), name='historico-list'),
    path('esp/events/', HistoricoCreateView.as_view(), name='esp-event'),
]
