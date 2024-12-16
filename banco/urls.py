from django.urls import path
from . import views
from .views import index, curtir_tirinha, comentar_tirinha
from usuarios.views import login


urlpatterns = [
    # path('login/', views.login, name='login'),  # Adicione a URL para a página de login
    path('', views.index, name='index'),
    path('add_tirinha/', views.add_tirinha, name="add_tirinha"),
    path('delete_tirinha/<int:tirinha_id>/', views.delete_tirinha, name='delete_tirinha'),
    path('delete_personagem/<int:personagem_id>/', views.delete_personagem, name='delete_personagem'),
    path('add_personagem/', views.add_personagem, name="add_personagem"),
    path('visualizar_personagens/', views.visualizar_personagens, name="visualizar_personagens"),
    # path('editar_perfil/', views.editar_perfil, name="editar_perfil"),
    path('curtir_tirinha/<int:tirinha_id>/', views.curtir_tirinha, name='curtir_tirinha'),
    path('comentar_tirinha/<int:tirinha_id>/', views.comentar_tirinha, name='comentar_tirinha'),
]
