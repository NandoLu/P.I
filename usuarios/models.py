from django.db import models
from django.contrib.auth.models import AbstractUser

class Users(AbstractUser):
    choices_cargo = (('A', 'Artista'),
                     ('U', 'Usuario'),
                     ('D', 'Administrador'))
    cargo = models.CharField(max_length=1, choices=choices_cargo)
    foto_perfil = models.ImageField(upload_to='foto_perfil/', blank=True, null=True)
