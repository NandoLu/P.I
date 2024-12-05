from rolepermissions.roles import AbstractUserRole

class Administrador(AbstractUserRole):
    available_permissions = {
        'cadastrar_produtos': True,
        'liberar_descontos': True,
        'cadastrar_artista': True,
    }

class Artista(AbstractUserRole):
    available_permissions = {
        'cadastrar_produtos': True,
    }   
    
class Usuario(AbstractUserRole):
    available_permissions = {
        'fazer_comentario': True,
        'fazer_curtida': True,
    }   

