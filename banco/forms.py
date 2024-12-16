# from django import forms
# from django.contrib.auth.forms import PasswordChangeForm
# from usuarios.models import Users

# class EditarPerfilForm(forms.ModelForm):
#     class Meta:
#         model = Users
#         fields = ['foto_perfil']

# class AlterarSenhaForm(PasswordChangeForm):
#     old_password = forms.CharField(
#         label="Senha Antiga",
#         strip=False,
#         widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True}),
#     )
#     new_password1 = forms.CharField(
#         label="Nova Senha",
#         strip=False,
#         widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
#         help_text="Sua senha deve ter pelo menos 8 caracteres e não pode ser muito comum.",
#     )
#     new_password2 = forms.CharField(
#         label="Confirme a Nova Senha",
#         strip=False,
#         widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
#     )

#     class Meta:
#         model = Users
#         fields = ['old_password', 'new_password1', 'new_password2']
