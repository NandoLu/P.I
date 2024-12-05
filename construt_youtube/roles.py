from rolepermissions.roles import AbstractUserRole

class Gerente(AbstractUserRole):
    available_permissions = {
        'cadastrar_produtos': True,
        'liberar_descontos': True,
        'cadastrar_artista': True,
    }

class Artista(AbstractUserRole):
    available_permissions = {
        'realizar_venda': True,
    }   
    

