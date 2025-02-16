from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import CustomUser


class CreateUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)

        common_classes = 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 shadow-sm'

        self.fields['username'].widget.attrs.update({
            'class': common_classes,
            'placeholder': "Entrez votre nom d'utilisateur"
        })
        self.fields['email'].widget.attrs.update({
            'class': common_classes,
            'placeholder': "Entrez votre adresse e-mail"
        })
        
        # Manually override password fields
        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'class': common_classes,
            'placeholder': "Entrez votre mot de passe"
        })
        self.fields['password2'].widget = forms.PasswordInput(attrs={
            'class': common_classes,
            'placeholder': "Confirmez votre mot de passe"
        })
