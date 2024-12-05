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
# somente quem tem a permissao consegue acessar a view

def index(request):
    return render(request, 'index.html')

def visualizar_artistas(request):
    artistas = Users.objects.filter(cargo="A")
    print(artistas)  # Adicione esta linha
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
        login = request.POST.get('email')
        senha = request.POST.get('senha')

        user = auth.authenticate(username=login, password=senha)

        if not user:
            # TODO Redirecionar com mensagem de erro
            return HttpResponse('Usuário inváido')
                
        auth.login(request, user)
        return redirect(reverse('plataforma'))  # Redireciona para a página 'plataforma' após login bem-sucedido

def logout(request):
    request.session.flush()
    return redirect(reverse('login'))

@has_permission_decorator('cadastrar_artista')
def excluir_usuario(request, id):
    artista = get_object_or_404(Users, id=id)
    artista.delete()
    messages.add_message(request, messages.SUCCESS, 'Artista excluido com sucesso')
    return redirect(reverse('cadastrar_artista'))

