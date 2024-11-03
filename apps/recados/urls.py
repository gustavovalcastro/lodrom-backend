from django.urls import path
from .views import RecadoCreateView, RecadoDeleteView, RecadoEditView, RecadoListView

urlpatterns = [
    path('recados/list/', RecadoListView.as_view(), name='recados-list'),
    path('recados/', RecadoCreateView.as_view(), name='recados'),
    path('recados/edit/<int:pk>', RecadoEditView.as_view(), name='recado-edit'),
    path('recados/delete/<int:pk>', RecadoDeleteView.as_view(), name='recado-delete'),
]
