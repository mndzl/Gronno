from django import forms
from .models import Project, Category
from django.forms import modelformset_factory

class CreateProject(forms.ModelForm):
    category = forms.ModelChoiceField(Category.objects.all(), label='Categoría', empty_label="Selecciona una categoría")
    title = forms.CharField(max_length=50, label='Título', widget=forms.TextInput(attrs={'placeholder':"Escribe aquí el título tu proyecto"}))
    description = forms.CharField(max_length=10000, label='Descripcion', widget=forms.Textarea(attrs={'placeholder':"Escribe aquí sobre tu proyecto"}))
    image1 = forms.ImageField()
    image2 = forms.ImageField()
    image3 = forms.ImageField()

    class Meta:
        model = Project
        fields = ['category','title','description','image1','image2','image3']
