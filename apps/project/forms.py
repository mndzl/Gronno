from django import forms
from .models import Project, Category

class CreateProject(forms.ModelForm):
    category = forms.ModelChoiceField(Category.objects.all(), required=True, label='Categoría', empty_label="Selecciona una categoría")
    title = forms.CharField(required=True, max_length=40, label='Título',widget=forms.TextInput(attrs={'placeholder':'Nombre del proyecto'}), error_messages={'unique': 'Ya existe un proyecto con este nombre.'})
    description = forms.CharField(
                                min_length=120,
                                max_length=10000,
                                label='Descripcion', 
                                widget=forms.Textarea(attrs={'placeholder':'Descripción del proyecto: muéstranos como lo pensaste, como te organizaste, y que cosas aprendiste de él'}), 
                                required=True)
    image1 = forms.ImageField(required=True)
    image2 = forms.ImageField(required=True)
    image3 = forms.ImageField(required=True)


    class Meta:
        model = Project
        fields = ['category','title','description','image1','image2','image3']
