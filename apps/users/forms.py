from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from apps.users.models import Gronner
from django_countries.fields import CountryField

class GronnerRegisterForm(UserCreationForm):
    email = forms.EmailField(error_messages={'unique': 'Este correo ya está asociado a una cuenta.'})
    username = forms.CharField(label='Nombre de usuario', error_messages={'unique': 'Ya existe un usuario con este nombre.'})
    first_name = forms.CharField(max_length=50, label='Nombre')
    last_name = forms.CharField(max_length=50, label='Apellido')
    dedication = forms.CharField(max_length=50, label='Ocupación')
    country = CountryField(blank_label='Selecciona un país').formfield(label='País')
    birth = forms.DateField(label='Fecha de nacimiento', widget=forms.DateInput(attrs={'placeholder':'dd/mm/aaaa'}))


    class Meta:
        model = User
        fields = ['first_name','last_name','username','password1','password2','email','country','birth','dedication']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']


class GronnerUpdateForm(forms.ModelForm):
    facebook = forms.CharField(max_length=50, required=False ,widget=forms.TextInput(attrs={'placeholder': 'Nombre de usuario'}))
    instagram = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'placeholder': 'Nombre de usuario'}))
    linkedin = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'placeholder': 'Nombre de usuario'}))
    twitter = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'placeholder': 'Nombre de usuario'}))
    extract = forms.CharField(required=False, widget=forms.Textarea(attrs={'placeholder': 'Cuéntanos sobre tí'}))
    class Meta:
        model = Gronner
        fields = ['extract', 'dedication', 'image', 'birth', 'country', 'facebook', 'instagram', 'linkedin', 'twitter', 'shows_email']
