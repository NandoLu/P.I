from django.shortcuts import render
from .models import Categoria, Tirinha, Imagem
from django.http import HttpResponse
from PIL import Image, ImageDraw
from datetime import date
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

def add_tirinha(request):
    if request.method == "GET":
        categorias = Categoria.objects.all()
        tirinhas = Tirinha.objects.all()
        return render(request, 'add_tirinha.html', {'categorias': categorias, 'tirinhas': tirinhas })
    elif request.method == "POST":
        nome = request.POST.get('nome')
        categoria = request.POST.get('categoria')
        imagens = request.FILES.getlist('imagens')

        tirinha = tirinha(nome=nome, 
                          categoria_id=categoria)
        tirinha.save()

        for f in request.FILES.getlist('imagens'):
            name = f'{date.today()}={tirinha.id}.jpg'

            img = Image.open(f)
            img = img.convert('RGB')
            img = img.resize((300,300))
            draw = ImageDraw.Draw(img)
            draw.text((20, 280), "poesia_em_tirinhas {date.today()}", (255, 255, 255))
            output = BytesIO()
            img.save(output, format="JPEG", quality=100)
            output.seek(0)
            img_final = InMemoryUploadedFile(output, 
                                            'ImageField',
                                            name,
                                            'image/jpeg',
                                            sys.getsizeof(output),
                                            None
            )

            # TODO Limitar tamanho de imagem
            img_dj = Imagem(imagem = img_final, tirinha=tirinha)
            img_dj.save()
        messages.add_message(request, messages.SUCCESS, 'tirinha adicionado com sucesso')

        return redirect(reverse('add_tirinha'))