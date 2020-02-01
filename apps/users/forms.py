from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from apps.users.models import Gronner, Dedication
from django_countries.fields import CountryField

class GronnerRegisterForm(UserCreationForm):
    email = forms.EmailField(error_messages={'unique': 'Este correo ya está asociado a una cuenta.'})
    username = forms.CharField(label='Nombre de usuario', error_messages={'unique': 'Ya existe un usuario con este nombre.'})
    first_name = forms.CharField(max_length=50, label='Nombres')
    last_name = forms.CharField(max_length=50, label='Apellidos')
    dedication = forms.ModelChoiceField(Dedication.objects.all(), label='Dedicación',empty_label="Selecciona una dedicación")
    country = CountryField(blank_label='Selecciona un país').formfield(label='Nacionalidad')
    birth = forms.DateField(label='Fecha de nacimiento', widget=forms.DateInput(attrs={'placeholder':'dd/mm/aaa'}))

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','country','birth','dedication','password1','password2']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']


class GronnerUpdateForm(forms.ModelForm):
    facebook = forms.CharField(max_length=50, required=False ,widget=forms.TextInput(attrs={'placeholder': 'Nombre de usuario'}))
    instagram = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'placeholder': 'Nombre de usuario'}))
    linkedin = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'placeholder': 'Nombre de usuario'}))
    extract = forms.CharField(required=False, widget=forms.Textarea(attrs={'placeholder': 'Cuéntanos sobre tí'}))
    class Meta:
        model = Gronner
        exclude = ['user', 'points']
