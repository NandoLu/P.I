from django.http import HttpResponse
from django.shortcuts import render
from rolepermissions.decorators import has_permission_decorator
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

def index(request):
    return render(request, 'index.html')

def visualizar_artistas(request):
    artistas = Users.objects.filter(cargo="A")
    print(artistas)  # Verifique se os artistas estão sendo recuperados
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
    if request.method == "GET":
        return render(request, 'cadastrar.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cargo = "U"
        foto_perfil = request.FILES.get('foto_perfil')
        if Users.objects.filter(username=username).exists(): 
            messages.error(request, 'Este nome de usuário já está em uso. Por favor, escolha outro.') 
            return redirect('cadastrar')
        if Users.objects.filter(email=email).exists(): 
            messages.error(request, 'Este e-mail de usuário já está em uso. Por favor, escolha outro.') 
            return redirect('cadastrar')
    try: 
        user = Users.objects.create_user(username=username, email=email, password=password, cargo=cargo, foto_perfil=foto_perfil) 
        user.save() 
        # Especificar o backend ao fazer login do usuário 
        auth_login(request, user, backend='seu_app.backends.EmailBackend')
        messages.success(request, 'Usuário cadastrado com sucesso') 
        return redirect('login') 
    except IntegrityError: 
        messages.error(request, 'Erro ao cadastrar usuário. Tente novamente.') 
        return redirect('cadastrar')


def logout(request):
    request.session.flush()
    return redirect(reverse('login'))

@has_permission_decorator('cadastrar_artista')
def excluir_usuario(request, id):
    artista = get_object_or_404(Users, id=id)
    artista.delete()
    messages.add_message(request, messages.SUCCESS, 'Artista excluido com sucesso')
    return redirect(reverse('cadastrar_artista'))