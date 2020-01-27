from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class GronnerRegisterForm(UserCreationForm):
    email = forms.EmailField()
    username = forms.CharField(label='Nombre de usuario')
    first_name = forms.CharField(max_length=50, label='Nombres')
    last_name = forms.CharField(max_length=50, label='Apellidos')
    dedication = forms.CharField(max_length=70, label='Dedicacion')

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','dedication','password1','password2']