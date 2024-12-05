from django.urls import path
from . import views

urlpatterns = [
    path('add_tirinha/', views.add_tirinha, name="add_tirinha")
]
