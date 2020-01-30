from django.shortcuts import render
from apps.project.models import Project, Comment
from apps.users.models import Gronner, Follow
from django.contrib.auth.models import User
import math
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin

class homepage(LoginRequiredMixin, ListView):
    model = Project
    context_object_name = 'projects'
    template_name = 'home/home.html'

    def get_queryset(self):
        user = self.request.user
        following = Follow.objects.filter(follower=user).values('following')
        return Project.objects.filter(author__in=following).order_by('-date_posted') | user.project_set.all().order_by('-date_posted')
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
                'gold':self.object_list[i].award_set.filter(medal__medal_type='Gold').count(),
                'silver':self.object_list[i].award_set.filter(medal__medal_type='Silver').count(),
                'bronze':self.object_list[i].award_set.filter(medal__medal_type='Bronze').count()
            }

        # Tendencia
        context["top_projects"] = Project.objects.all().order_by('points')[:5]
 
        # Otros
        context["medals"] = medals
        context["projects"] = zip(self.object_list,comments, medals)
        context["personal_projects"] = user.project_set.all().order_by('-date_posted')
        return context
    
    
    