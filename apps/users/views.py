from django.shortcuts import render, redirect
from apps.project.models import Category, Project
from apps.users.models import Gronner
from django.utils import timezone
import datetime
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import GronnerRegisterForm, UserUpdateForm, GronnerUpdateForm
from django.contrib.auth.decorators import login_required
from .forms import GronnerRegisterForm
from django.contrib import messages

# Create your views here.

@login_required
def profile(request):

    # Inicializacion 
    categories = []

    # Busqueda de perfil
    gronner = request.user
    
    # Obtener todos los proyectos del usuario
    projects = gronner.project_set.all().order_by('-date_posted')

    # Proyectos recientes
    recents = gronner.project_set.filter(date_posted__gte=timezone.now()-datetime.timedelta(days=31), date_posted__lte=timezone.now()).order_by('-date_posted')

    # Obtener las categorias en las que el usuario participo
    for project in projects:
        if project.category not in categories:
            categories.append(project.category)

    maxprojects = 0
    categorychosen = None

    # Obtener la categoria con mas proyectos subidos
    for category in categories:
        quantity = category.project_set.filter(author=gronner).count()
        if quantity > maxprojects:
            maxprojects = quantity
            categorychosen = category

    # Obtener las redes sociales del usuario
    social = gronner.social_media_set.all()

    # Project per category
    relation = [[0] for i in range(len(categories))]

    for i in range(len(categories)):
        relation[i] = gronner.project_set.filter(category=categories[i]).order_by('-date_posted')

    # Obtencion de medallas
    medals = [{}] * len(projects)
    for i in range(len(projects)):
        medals[i] = {
            'gold':projects[i].award_set.filter(medal__medal_type='Gold').count(),
            'silver':projects[i].award_set.filter(medal__medal_type='Silver').count(),
            'bronze':projects[i].award_set.filter(medal__medal_type='Bronze').count()
        }

    # Update
    if request.method == 'POST':
        form_u = UserUpdateForm(request.POST, instance=request.user)
        form_g = GronnerUpdateForm(request.POST,request.FILES, instance=request.user.gronner)
        if form_g.is_valid():
            form_g.save()
            messages.success(request, 'Tu perfil ha sido actualizado.')
            return redirect('profile')
        if form_u.is_valid():
            form_g.save()
            messages.success(request, 'Tu perfil ha sido actualizado.')
            return redirect('profile')
    else:
        form_u = UserUpdateForm(instance=request.user)
        form_g = GronnerUpdateForm(instance=request.user)


    # Definicion del contexto
    context = {
        'categories':categories,
        'fav_category':categorychosen,
        'projects':projects,
        'socials':social,
        'recents':zip(recents,medals),
        'user':gronner,
        'extract_length':len(gronner.gronner.extract),
        'per_category':zip(relation,categories),
        'form_u':form_u,
        'form_g':form_g
    }


    return render(request, 'users/users.html', context)

def register(request):
    if request.method == 'POST':
        form = GronnerRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            dedication = form.cleaned_data.get('dedication')
            username = form.cleaned_data.get('username')
            Gronner.objects.create(user=User.objects.filter(username=username).first(), dedication=dedication)
            return redirect('login')
    else:
        form = GronnerRegisterForm()
    return render(request, 'users/register.html',{'form':form})
