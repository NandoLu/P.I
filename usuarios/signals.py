from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Users
from rolepermissions.roles import assign_role # qual class ele tem

@receiver(post_save, sender=Users)
def define_permissoes(sender, instance, created, **kwargs):
    if created:
        if instance.cargo == "A":
            assign_role(instance, 'artista')
        elif instance.cargo == "D":
            assign_role(instance, 'administrador')
