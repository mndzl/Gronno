from django.shortcuts import render
from apps.project.models import Project, Comment
from django.contrib.auth.models import User


def homepage(request):
    projects = Project.objects.all()
    comments = []

    for project in projects:
        comments.append(project.comment_set.all().count())

    context = {
        'projects':zip(projects,comments),
        'personal_projects':User.objects.filter(username='mendezluis').first().project_set.all()
    }


    return render(request, 'home/home.html',context)