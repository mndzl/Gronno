from django import forms
from apps.users.models import Gronner
from django.contrib.auth.forms import UserCreationForm

class GronnerRegisterForm(UserCreationForm):
    email = forms.EmailField()
    username = forms.CharField(label='Nombre de usuario')
    full_name = forms.CharField(max_length=50, label='Nombre completo')

    class Meta:
        model = Gronner
        fields = ['username','full_name','email','password1','password2']