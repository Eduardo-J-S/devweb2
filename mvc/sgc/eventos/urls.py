from django.urls import path

from . import views 

urlpatterns = [
    path('selecionar/', views.selecionar_projeto, name='selecionar_projeto'),
    path('<int:projeto_id>/eventos/', views.listar_eventos, name='listar_eventos'),
    path('<int:projeto_id>/eventos/novo/', views.criar_evento, name='criar_evento'),
]