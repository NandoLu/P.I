from django.shortcuts import render, redirect, get_object_or_404
from .models import Personagem, Tirinha, Imagem, Curtida, Comentario
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
from django.contrib.auth.decorators import login_required
# from .forms import EditarPerfilForm, AlterarSenhaForm
# from django.contrib.auth import update_session_auth_hash
# from django.http import JsonResponse
# from usuarios.views import login

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

def delete_personagem(request, personagem_id):
    personagem = get_object_or_404(Personagem, id=personagem_id)
    personagem.delete()
    messages.add_message(request, messages.SUCCESS, 'Personagem excluído com sucesso')
    return redirect(reverse('add_personagem'))


@login_required
def add_tirinha(request):
    if request.method == "GET":
        if request.user.cargo == 'D':
            personagens = Personagem.objects.all()
            tirinhas = Tirinha.objects.all()
        else:
            personagens = Personagem.objects.filter(artista=request.user)
            tirinhas = Tirinha.objects.filter(personagem__artista=request.user)
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
            img = img.resize((600, 600))
            draw = ImageDraw.Draw(img)
            draw.text((20, 580), f"poesia_em_tirinhas {date.today()}", (255, 255, 255))
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

@login_required
def delete_tirinha(request, tirinha_id):
    try:
        tirinha = get_object_or_404(Tirinha, id=tirinha_id)
        if tirinha.personagem.artista == request.user or request.user.cargo == 'D':
            tirinha.delete()
            messages.add_message(request, messages.SUCCESS, 'Tirinha excluída com sucesso')
        else:
            messages.add_message(request, messages.ERROR, 'Você não tem permissão para excluir esta tirinha')
    except Tirinha.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'Tirinha não encontrada')
    return redirect(reverse('add_tirinha'))

def visualizar_personagens(request):
    personagens = Personagem.objects.all()
    print(personagens)  # Verifique se os persoangens estão sendo recuperados
    return render(request, 'visualizar_personagens.html', {'personagens': personagens})

# @login_required
# def editar_perfil(request):
#     if request.method == 'POST':
#         perfil_form = EditarPerfilForm(request.POST, request.FILES, instance=request.user)
#         senha_form = AlterarSenhaForm(request.user, request.POST)
#         if perfil_form.is_valid() and senha_form.is_valid():
#             perfil_form.save()
#             user = senha_form.save()
#             update_session_auth_hash(request, user)  # Atualiza a sessão com a nova senha
#             messages.success(request, 'Seu perfil e senha foram atualizados com sucesso!')
#         elif perfil_form.is_valid():
#             perfil_form.save()
#             messages.success(request, 'Seu perfil foi atualizado com sucesso!')
#         elif senha_form.is_valid():
#             user = senha_form.save()
#             update_session_auth_hash(request, user)  # Atualiza a sessão com a nova senha
#             messages.success(request, 'Sua senha foi atualizada com sucesso!')
#         else:
#             messages.error(request, 'Por favor, corrija os erros abaixo.')
#         return redirect('editar_perfil')
#     else:
#         perfil_form = EditarPerfilForm(instance=request.user)
#         senha_form = AlterarSenhaForm(request.user)
#     return render(request, 'editar_perfil.html', {
#         'perfil_form': perfil_form,
#         'senha_form': senha_form
#     })


def index(request):
    tirinhas = Tirinha.objects.all().order_by('-id')[:10]
    imagens = Imagem.objects.filter(tirinha__in=tirinhas)
    return render(request, 'index.html', {'tirinhas': tirinhas, 'imagens': imagens, 'is_authenticated': request.user.is_authenticated})

def curtir_tirinha(request, tirinha_id):
    if not request.user.is_authenticated:
        return redirect('login')  # Redireciona para a página de login
    tirinha = get_object_or_404(Tirinha, id=tirinha_id)
    curtida, created = Curtida.objects.get_or_create(usuario=request.user, tirinha=tirinha)
    if not created:
        curtida.delete()
    return redirect(f'/banco/?modal={tirinha_id}')

def comentar_tirinha(request, tirinha_id):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')  # Redireciona para a página de login
        tirinha = get_object_or_404(Tirinha, id=tirinha_id)
        texto = request.POST.get('texto')
        Comentario.objects.create(usuario=request.user, tirinha=tirinha, texto=texto)
    return redirect(f'/banco/?modal={tirinha_id}')
