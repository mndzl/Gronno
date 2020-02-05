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
    trending = {
        'projects':Project.objects.filter(is_active = True, category__in = request.user.gronner.categories_followed.all())[:20],
        'categories':Category.objects.all()
    }

    if query:
        trending = None
        projects = Project.objects.filter(
            Q(title__icontains = query) |
            Q(description__icontains = query),
            is_active = True
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
        'categories': categories,
        'trending':trending
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
        user = self.request.user

        # Comments
        comments = []   
        for project in self.object_list:
            comm = project.comment_set.all().count()
            if comm>999:
                comm=str(round(10722/1000,1)) + 'k'
            comments.append(comm)
        context["comments"] = comments

        # Obtencion de medallas
        medals = [{}] * len(self.object_list)
        for i in range(len(self.object_list)):
            medals[i] = {
                'gold':len(self.object_list[i].award_set.filter(medal__medal_type='Gold')),
                'silver':len(self.object_list[i].award_set.filter(medal__medal_type='Silver')),
                'bronze':len(self.object_list[i].award_set.filter(medal__medal_type='Bronze'))
            }

        context["medals"] = medals
        context["projects"] = zip(self.object_list,comments, medals)
        
        return context
    
    
