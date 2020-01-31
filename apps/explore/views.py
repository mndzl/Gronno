from django.shortcuts import render
from apps.project.models import Project, Category
from django.views.generic import ListView



class CategoryExplore(ListView):
    model = Project
    context_object_name = 'projects'
    template_name = 'explore/category_explore.html'
    
    def get_queryset(self, **kwargs):
        category = self.kwargs.get('category')
        return Project.objects.filter(category__diminutive=category).order_by('-points')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = Category.objects.get(diminutive=self.kwargs.get('category'))
        return context
    
    
