from django.shortcuts import render
from apps.project.models import Project, Comment
from apps.users.models import Gronner
from django.contrib.auth.models import User
import math
from django.contrib.auth.decorators import login_required

@login_required
def homepage(request):
    projects = Project.objects.all().order_by('-date_posted')
    comments = []
    user = request.user

    for project in projects:
        comm = project.comment_set.all().count()
        if comm>999:
            comm=str(round(10722/1000,1)) + 'k'
        comments.append(comm)

    
    # Obtencion de medallas
    medals = [{}] * len(projects)
    for i in range(len(projects)):
        medals[i] = {
            'gold':projects[i].award_set.filter(medal__medal_type='Gold').count(),
            'silver':projects[i].award_set.filter(medal__medal_type='Silver').count(),
            'bronze':projects[i].award_set.filter(medal__medal_type='Bronze').count()
        }


    context = {
        'projects':zip(projects,comments, medals),
        'personal_projects':user.project_set.all().order_by('-date_posted'),
        'user':user
    }


    return render(request, 'home/home.html',context)