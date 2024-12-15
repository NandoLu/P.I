from django.db import models
from usuarios.models import Users

class Personagem(models.Model):
    nome = models.CharField(max_length=40)
    artista = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True)
    imagem = models.ImageField(upload_to="imagem_personagem", default='media/imagex.jpg')
    descricao = models.TextField(blank=True, null=True)  # Novo campo para descrição

    def __str__(self):
        return self.nome

class Tirinha(models.Model):
    titulo = models.CharField(max_length=40)
    personagem = models.ForeignKey(Personagem, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.titulo

class Imagem(models.Model):
    imagem = models.ImageField(upload_to="imagem_tirinha")
    tirinha = models.ForeignKey(Tirinha, on_delete=models.CASCADE)

class Curtida(models.Model):
    usuario = models.ForeignKey(Users, on_delete=models.CASCADE)
    tirinha = models.ForeignKey(Tirinha, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'tirinha')

class Comentario(models.Model):
    usuario = models.ForeignKey(Users, on_delete=models.CASCADE)
    tirinha = models.ForeignKey(Tirinha, on_delete=models.CASCADE)
    texto = models.TextField()
    data = models.DateTimeField(auto_now_add=True)
