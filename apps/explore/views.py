from django.shortcuts import render
from apps.project.models import Project, Category
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.db.models import Q

def Explore(request):
    query = request.GET.get('search')
    projects = None
    users = None
    categories = None
    if query:
        projects = Project.objects.filter(
            Q(title__icontains = query) |
            Q(description__icontains = query)
        ).order_by('-points')

        users = User.objects.filter(
            Q(username__icontains = query) |
            Q(first_name__icontains = query) |
            Q(last_name__icontains = query)
        ).order_by('-gronner__points').distinct()

        categories = Category.objects.filter(
            Q(name__icontains = query) |
            Q(diminutive__icontains = query)
        ).distinct()

    context = {
        'projects': projects,
        'users': users,
        'categories': categories
    }
    return render(request, 'explore/explore.html', context)

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
    
    
