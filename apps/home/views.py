from django.shortcuts import render
from apps.project.models import Project, Comment
from apps.users.models import Gronner
import math

def homepage(request):
    projects = Project.objects.all().order_by('-date_posted')
    comments = []
    user = Gronner.objects.filter(username='luismendezg').first()

    for project in projects:
        comm = project.comment_set.all().count()
        if comm>999:
            comm=str(round(10722/1000,1)) + 'k'
        comments.append(comm)

    context = {
        'projects':zip(projects,comments),
        'personal_projects':user.project_set.all().order_by('-date_posted'),
        'user':user
    }


    return render(request, 'home/home.html',context)