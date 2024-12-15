from rolepermissions.roles import AbstractUserRole

class Administrador(AbstractUserRole):
    available_permissions = {
        'cadastrar_tirinhas': True,
        'cadastrar_artista': True,
    }

class Artista(AbstractUserRole):
    available_permissions = {
        'cadastrar_tirinhas': True,
    }   
    
class Usuario(AbstractUserRole):
    available_permissions = {
        'fazer_comentario': True,
        'fazer_curtida': True,
    }   
