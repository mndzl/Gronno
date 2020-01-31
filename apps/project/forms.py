from django import forms
from .models import Project
from .models import Category

class CreateProject(forms.ModelForm):
    category = forms.ModelChoiceField(Category.objects.all(), label='Categoría', empty_label="Selecciona una categoría")
    title = forms.CharField(max_length=50, label='Título', initial="Escribe aquí el título de tu proyecto")
    description = forms.CharField(max_length=10000, label='Descripcion', initial="Escribe aquí sobre tu proyecto")
    class Meta:
        model = Project
        fields = ['category','title','description']