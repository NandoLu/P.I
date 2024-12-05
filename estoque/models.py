from pyexpat import model
from django.db import models

class Categoria(models.Model):
    titulo = models.CharField(max_length=40)

    def __str__(self):
        return self.titulo
    
class Tirinha(models.Model):
    nome = models.CharField(max_length=40)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.nome

class Imagem(models.Model):
    imagem = models.ImageField(upload_to="imagem_tirinha")
    tirinha = models.ForeignKey(Tirinha, on_delete=models.CASCADE)

    