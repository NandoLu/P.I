from django.http import HttpResponse
from django.shortcuts import render
from rolepermissions.decorators import has_permission_decorator
from django.contrib.auth.decorators import login_required
from rolepermissions.roles import assign_role
from .models import Users
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import auth
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.db import IntegrityError
# somente quem tem a permissao consegue acessar a view
from banco.models import Tirinha, Imagem, Personagem
from .forms import EditarFotoPerfilForm, AlterarSenhaForm
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
# from .views import login

def index(request):
    tirinhas = Tirinha.objects.all().order_by('-id')[:10]  # Busca as 10 tirinhas mais recentes
    imagens = Imagem.objects.filter(tirinha__in=tirinhas)
    return render(request, 'index.html', {'tirinhas': tirinhas, 'imagens': imagens})

def visualizar_artistas(request):
    artistas = Users.objects.filter(cargo="A").prefetch_related('personagem_set')
    return render(request, 'visualizar_artistas.html', {'artistas': artistas})

@has_permission_decorator('cadastrar_artista')
def cadastrar_artista(request):
    if request.method == "GET":
        artistas = Users.objects.filter(cargo="A")
        return render(request, 'cadastrar_artista.html', {'artistas': artistas})
    if request.method == "POST":
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        #TODO: Fazer validações dos dados
        
        user = Users.objects.filter(email=email)

        if user.exists():
            # TODO: utilizar messages do django
            return HttpResponse('Email já existe')
        
        user = Users.objects.create_user(username=email, 
                                        email=email,
                                        password=senha,
                                        first_name=nome,
                                        last_name=sobrenome,
                                        cargo="A")
        # TODO redirecionar com uma mensagem
        messages.add_message(request, messages.SUCCESS, 'Artista cadastrado com sucesso')
        return redirect(reverse('cadastrar_artista'))

def login(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect(reverse('plataforma'))
        return render(request, 'login.html')
    elif request.method == "POST":
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        user = auth.authenticate(username=email, password=senha)

        if not user:
            messages.add_message(request, messages.ERROR, 'Usuário inválido')
            return redirect(reverse('login'))
                
        auth.login(request, user)
        return redirect(reverse('plataforma'))

def cadastrar(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        foto_perfil = request.FILES.get('foto_perfil')

        # TODO: Fazer validações dos dados

        user = Users.objects.filter(email=email)

        if user.exists():
            messages.error(request, 'Email já existe')
            return redirect('cadastrar')

        user = Users.objects.create_user(username=email, 
                                         email=email,
                                         password=password,
                                         first_name=first_name,
                                         last_name=last_name,
                                         foto_perfil=foto_perfil)
        messages.success(request, 'Usuário cadastrado com sucesso')
        return redirect('login')
    return render(request, 'cadastrar.html')

def logout(request):
    request.session.flush()
    return redirect(reverse('login'))

@has_permission_decorator('cadastrar_artista')
def excluir_usuario(request, id):
    artista = get_object_or_404(Users, id=id)
    artista.delete()
    messages.add_message(request, messages.SUCCESS, 'Artista excluido com sucesso')
    return redirect(reverse('cadastrar_artista'))


from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from .forms import UserChangeForm, EditarFotoPerfilForm, AlterarSenhaForm

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from .forms import UserChangeForm, EditarFotoPerfilForm, AlterarSenhaForm

@login_required
def editar_perfil(request):
    usuario_form = UserChangeForm(instance=request.user)
    foto_form = EditarFotoPerfilForm(instance=request.user)
    senha_form = AlterarSenhaForm(request.user)

    if request.method == 'POST':
        if 'salvar_usuario' in request.POST:
            usuario_form = UserChangeForm(request.POST, instance=request.user)
            if usuario_form.is_valid():
                usuario_form.save()
                messages.success(request, 'Seu nome de usuário e email foram atualizados com sucesso!')
                return redirect('editar_perfil')
        elif 'salvar_foto' in request.POST:
            foto_form = EditarFotoPerfilForm(request.POST, request.FILES, instance=request.user)
            if foto_form.is_valid():
                foto_form.save()
                messages.success(request, 'Sua foto de perfil foi atualizada com sucesso!')
                return redirect('editar_perfil')
        elif 'salvar_senha' in request.POST:
            senha_form = AlterarSenhaForm(request.user, request.POST)
            if senha_form.is_valid():
                user = senha_form.save()
                update_session_auth_hash(request, user)  # Atualiza a sessão com a nova senha
                messages.success(request, 'Sua senha foi atualizada com sucesso!')
                return redirect('editar_perfil')
            else:
                messages.error(request, 'Por favor, corrija os erros abaixo.')

    return render(request, 'editar_perfil.html', {
        'usuario_form': usuario_form,
        'foto_form': foto_form,
        'senha_form': senha_form
    })
