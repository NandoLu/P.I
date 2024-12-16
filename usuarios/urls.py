from django.urls import path
from . import views

urlpatterns = [
    path('plataforma/', views.index, name="plataforma"), 
    path('cadastrar_artista/', views.cadastrar_artista, name="cadastrar_artista"), 
    path('visualizar_artistas/', views.visualizar_artistas, name="visualizar_artistas"), 
    path('login/', views.login, name="login"),
    path('sair/', views.logout, name="sair"),
    path('cadastrar/', views.cadastrar, name="cadastrar"),
    path('editar_perfil/', views.editar_perfil, name="editar_perfil"),
    path('excluir_usuario/<str:id>/', views.excluir_usuario, name="excluir_usuario" ),
]
