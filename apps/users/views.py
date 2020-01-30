from django.shortcuts import render, redirect, get_object_or_404
from apps.project.models import Category, Project
from apps.users.models import Gronner, Follow
from django.utils import timezone
import datetime
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import GronnerRegisterForm, UserUpdateForm, GronnerUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .forms import GronnerRegisterForm
from django.contrib import messages
from django.core.mail import EmailMessage
# Create your views here.

class Profile(ListView):
    model = Project
    template_name = 'users/users.html'
    context_object_name = 'projects'

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

        # Obtener las redes sociales del usuario
        social = user.social_media_set.all()
        context['socials'] = social

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

        # Adicionales
        context['recents'] = zip(self.object_list,medals)
        context['extract_length'] = len(user.gronner.extract),
        context['per_category'] = zip(relation,categories)
        context['followers'] = Follow.objects.filter(following=user).count()

        # Update
        if self.request.method == 'POST':
            form_g = GronnerUpdateForm(self.request.POST,self.request.FILES, instance=user.gronner)
            if form_g.is_valid():
                form_g.save()
                messages.success(self.request, 'Tu perfil ha sido actualizado.')
                return redirect('profile')
        else:
            form_g = GronnerUpdateForm(instance=user)

        context['form_g'] = form_g

        return context
    
def register(request):
    if request.method == 'POST':
        form = GronnerRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            dedication = form.cleaned_data.get('dedication')
            username = form.cleaned_data.get('username')
            Gronner.objects.create(user=User.objects.filter(username=username).first(), dedication=dedication)
            newuser = User.objects.filter(username=username).first()
            email = EmailMessage(
                '¡Bienvenido/a a Gronno!',
                'Que fue mi panaaaaaaaaaaaa',
                to=[newuser.email]
            )
            email.send()
            return redirect('login')
    else:
        form = GronnerRegisterForm()
    return render(request, 'users/register.html',{'form':form})
