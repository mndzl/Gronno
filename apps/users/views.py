from django.shortcuts import render, redirect, get_object_or_404
from apps.project.models import Category, Project
from apps.users.models import Gronner, Follow
from django.utils import timezone
import datetime
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import GronnerRegisterForm, UserUpdateForm, GronnerUpdateForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, UpdateView
from .forms import GronnerRegisterForm
from django.contrib import messages
from django.core.mail import EmailMessage
# Create your views here.

class Profile(ListView):
    model = Project
    template_name = 'users/users.html'
    context_object_name = 'projects'

    def get_success_url(self):
        return redirect("profile")

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Project.objects.filter(author=user, date_posted__gte=timezone.now()-datetime.timedelta(days=31), date_posted__lte=timezone.now()).order_by('-date_posted')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obteniendo Usuario
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        context["visiting"] = user
        
        # Obteniendo categorias
        categories = []
        for project in self.object_list:
            if project.category not in categories:
                categories.append(project.category)

        context['categories'] = categories

        # Projectos por categoria
        relation = [[0] for i in range(len(categories))]
        for i in range(len(categories)):
            relation[i] = user.project_set.filter(category=categories[i]).order_by('-date_posted')

        # Obtener la categoria con mas proyectos subidos
        maxprojects = 0
        categorychosen = None

        for category in categories:
            quantity = category.project_set.filter(author=user).count()
            if quantity > maxprojects:
                maxprojects = quantity
                categorychosen = category
        
        context['fav_category'] = categorychosen

        # Obtencion de medallas
        medals = [{}] * len(self.object_list)
        for i in range(len(self.object_list)):
            medals[i] = {
                'gold':self.object_list[i].award_set.filter(medal__medal_type='Gold').count(),
                'silver':self.object_list[i].award_set.filter(medal__medal_type='Silver').count(),
                'bronze':self.object_list[i].award_set.filter(medal__medal_type='Bronze').count()
            }
        context['medals'] = medals

        # Obteniendo Redes Sociales
        socials = [{}]

        if user.gronner.facebook is not '':
            socials.append({'name':'facebook', 'link':f'https://www.facebook.com/{user.gronner.facebook}', 'color':'#3b5998'})

        if user.gronner.instagram is not '':
            socials.append({'name':'instagram', 'link':f'https://www.instagram.com/{user.gronner.instagram}', 'color':'#8f0047'})

        if user.gronner.twitter is not '':
            socials.append({'name':'twitter', 'link':f'https://www.twitter.com/{user.gronner.twitter}', 'color':'#00acee' })

        if user.gronner.linkedin is not '':
            socials.append({'name':'linkedin', 'link':f'https://www.linkedin.com/in/{user.gronner.linkedin}', 'color':'#0e76a8'})
        
        context['socials'] = socials

        # Adicionales
        context['recents'] = zip(self.object_list,medals)
        context['extract_length'] = len(user.gronner.extract)
        context['per_category'] = zip(relation,categories)
        context['followers'] = Follow.objects.filter(following=user).count()

        return context     
    
def register(request):
    if request.method == 'POST':
        form = GronnerRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            dedication = form.cleaned_data.get('dedication')
            username = form.cleaned_data.get('username')
            country = form.cleaned_data.get('country')
            newuser = User.objects.filter(username=username).first()
            Gronner.objects.create(user=newuser, dedication=dedication, country=country)
            email = EmailMessage(
                '¡Bienvenido/a a Gronno!',
                'This is email content',
                to=[newuser.email]
            )
            email.send()
            return redirect('login')
    else:
        form = GronnerRegisterForm()
    return render(request, 'users/register.html',{'form':form})

@login_required
def ProfileUpdateView(request):
    user = get_object_or_404(User, username=request.user.username)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=user)
        g_form = GronnerUpdateForm(request.POST, request.FILES, instance=user.gronner)
        
        if u_form.is_valid() and g_form.is_valid():
            user_form = u_form.save(commit=False)
            gronner_form = g_form.save(commit=False)
            gronner_form.user = user_form
            user_form.save()
            gronner_form.save()
            return redirect('profile', user_form.username)
    
    else:
        u_form = UserUpdateForm(instance=user)
        g_form = GronnerUpdateForm(instance=user.gronner)
    
    return render(request, 'users/configuration.html', {'u_form':u_form, 'g_form':g_form})


    
