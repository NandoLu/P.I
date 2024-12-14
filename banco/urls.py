from django.urls import path
from . import views

urlpatterns = [
    path('add_tirinha/', views.add_tirinha, name="add_tirinha"),
    path('add_personagem/', views.add_personagem, name="add_personagem"),
    path('visualizar_personagens/', views.visualizar_personagens, name="visualizar_personagens")
]