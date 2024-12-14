from django.shortcuts import render
from .models import Personagem, Tirinha, Imagem
from usuarios.models import Users
from django.http import HttpResponse
from PIL import Image, ImageDraw
from datetime import date
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

def add_personagem(request): 
    if request.method == "GET": 
        artistas = Users.objects.filter(cargo="A") 
        personagens = Personagem.objects.all() 
        return render(request, 'add_personagem.html', {'artistas': artistas, 'personagens': personagens}) 
    elif request.method == "POST": 
        nome = request.POST.get('nome') 
        artista_id = request.POST.get('artista') 
        imagem = request.FILES.get('imagem') 
        descricao = request.POST.get('descricao') 
        personagem = Personagem(nome=nome, artista_id=artista_id, imagem=imagem, descricao=descricao) 
        personagem.save() 
        messages.add_message(request, messages.SUCCESS, 'Personagem adicionado com sucesso') 
        return redirect(reverse('add_personagem'))

def add_tirinha(request):
    if request.method == "GET":
        personagens = Personagem.objects.all()
        tirinhas = Tirinha.objects.all()
        return render(request, 'add_tirinha.html', {'personagens': personagens, 'tirinhas': tirinhas})
    elif request.method == "POST":
        titulo = request.POST.get('titulo')
        personagem_id = request.POST.get('personagem')
        imagens = request.FILES.getlist('imagens')

        tirinha = Tirinha(titulo=titulo, personagem_id=personagem_id)
        tirinha.save()

        for f in imagens:
            name = f'{date.today()}={tirinha.id}.jpg'

            img = Image.open(f)
            img = img.convert('RGB')
            img = img.resize((200, 200))
            draw = ImageDraw.Draw(img)
            draw.text((20, 180), f"poesia_em_tirinhas {date.today()}", (255, 255, 255))
            output = BytesIO()
            img.save(output, format="JPEG", quality=100)
            output.seek(0)
            img_final = InMemoryUploadedFile(output, 
                                             'ImageField', 
                                             name, 
                                             'image/jpeg', 
                                             sys.getsizeof(output), 
                                             None)

            img_dj = Imagem(imagem=img_final, tirinha=tirinha)
            img_dj.save()
        
        messages.add_message(request, messages.SUCCESS, 'Tirinha adicionada com sucesso')

        return redirect(reverse('add_tirinha'))

def visualizar_personagens(request):
    personagens = Personagem.objects.all()
    print(personagens)  # Verifique se os persoangens estão sendo recuperados
    return render(request, 'visualizar_personagens.html', {'personagens': personagens})