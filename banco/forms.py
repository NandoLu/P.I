from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from .models import Users

class EditarPerfilForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['foto_perfil']

class AlterarSenhaForm(PasswordChangeForm):
    class Meta:
        model = Users
        fields = ['old_password', 'new_password1', 'new_password2']
