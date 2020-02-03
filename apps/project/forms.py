from django import forms
from .models import Project, Category
from django.forms import modelformset_factory

class CreateProject(forms.ModelForm):
    category = forms.ModelChoiceField(Category.objects.all(), label='Categoría', empty_label="Selecciona una categoría")
    title = forms.CharField(max_length=50, label='Título', initial='Nombre del proyecto')
    description = forms.CharField(min_length=150, max_length=10000, label='Descripcion', initial='Descripción del proyecto: muéstranos como lo pensaste, como te organizaste, y que cosas aprendiste de él')
    image1 = forms.ImageField(required=False)
    image2 = forms.ImageField(required=False)
    image3 = forms.ImageField(required=False)

    class Meta:
        model = Project
        fields = ['category','title','description','image1','image2','image3']
