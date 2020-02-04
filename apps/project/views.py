from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, FormView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Project, Comment, Award, Medal, Report
from django.shortcuts import redirect
from apps.home.views import homepage
from django.contrib.auth.models import User
from .forms import CreateProject
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import modelformset_factory
from django.contrib import messages
from PIL import ImageFile
from django.core.mail import EmailMessage


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    object_list = None
    object = None
    template_name = 'project/project_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        this_object = self.get_object()
        context["comments"] = this_object.comment_set.all().order_by('-date_commented')
        context['project'] = this_object
        
        # Tendencia
        context["top_projects"] = Project.objects.filter(is_active=True).order_by('points')[:5]
        context["personal_projects"] = self.request.user.project_set.filter(is_active=True).order_by('-date_posted')
        context["top_users"] = User.objects.all().order_by('gronner__points')[:3]
        return context

    def post(self, request, pk):
        text = request.POST.get('comment')
        Comment.objects.create(user=request.user, text=text, project=self.get_object())

        return redirect(self.request.path_info)

class MedalToggle(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        post_id = self.kwargs.get('pk')
        obj = get_object_or_404(Project, id=post_id)
        url_ = obj.get_absolute_url()
        user = self.request.user
        medal_request = self.kwargs.get('medal')
        medal = Medal.objects.get(medal_type=medal_request)
        medals_user = Award.objects.filter(user=user, project=obj)
        calified = bool(medals_user.count())

        if not calified:
            new_medal = Award.objects.create(user=user, medal=medal, project=obj)
            obj.author.gronner.points += new_medal.medal.points
            obj.author.gronner.save()
        else: 
            if(medals_user.first().medal!=medal):
                obj.author.gronner.points -=  medals_user.first().medal.points
                medals_user.first().delete()
                new_medal = Award.objects.create(user=user, medal=medal, project=obj)
                obj.author.gronner.points +=  new_medal.medal.points
                obj.author.gronner.save()
            else:
                obj.author.gronner.points -=  medals_user.first().medal.points
                obj.author.gronner.save()
                medals_user.first().delete()

        return url_

class ProjectCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Project
    form_class = CreateProject
    success_message = "Tu proyecto se ha subido correctamente"
    ImageFile.LOAD_TRUNCATED_IMAGES = True

    def form_valid(self, form):
        form.instance.author = self.request.user
        self.request.user.gronner.points += 500
        self.request.user.gronner.save()
        return super().form_valid(form)
    

class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    form_class = CreateProject
    template_name_suffix = '_update_form'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        project = self.get_object()
        if project.author == self.request.user:
            return True
        return False
    

class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model = Project
    success_url = '/'
    success_message = "Tu proyecto se ha eliminado."

    def test_func(self):
        project = self.get_object()
        if project.author == self.request.user:
            return True
        project.author.gronner.points -= 500
        project.author.gronner.save()
        return False

def suspend(project, reason):
    project.is_active = False
    project.author.gronner.points -= 500
    email = EmailMessage(
        'Proyecto eliminado',
        f"""Lo sentimos, tu proyecto {project.title} ha sido eliminado debido a que 
            la comunidad lo ha reportado por la siguiente razon: {reason}.""",
        to=[project.author.email]
    )
    email.send()
    project.save()
    project.author.save()

class ReportProject(LoginRequiredMixin, RedirectView):
    reasons = ['El proyecto no es de la categoría indicada', 'Uso inapropiado del lenguaje', 'No es un proyecto']

    def get_redirect_url(self, *args, **kwargs):
        post_id = self.kwargs.get('pk')
        reason = self.kwargs.get('reason')
        user = self.request.user
        obj = get_object_or_404(Project, id=post_id)
        reports_user = len(Report.objects.filter(user=user, project=obj))
        reports_project_reason = len(obj.report_set.filter(reason = self.reasons[reason]))
        reported = bool(reports_user)

        if not reported:
            Report.objects.create(user=user, reason=self.reasons[reason], project=obj)
            messages.add_message(self.request, messages.INFO, 'Tu reporte ha sido tomado, gracias por contribuir a la comunidad.')        
            if reports_project_reason >= 10:
                suspend(project=obj, reason=self.reasons[reason])

        return reverse('homepage')

class CommentDelete(LoginRequiredMixin, UserPassesTestMixin, RedirectView):
    def test_func(self):
        project_id = self.kwargs.get('pk_project')
        project = Project.objects.get(id=project_id)
        if project.author == self.request.user:
            return True
        return False

    def get_redirect_url(self, *args, **kwargs):
        post_id = self.kwargs.get('pk_project')
        post = Project.objects.get(id=post_id)
        url_ = post.get_absolute_url()
        comment_id = self.kwargs.get('pk_comment')
        comment = Comment.objects.get(id=comment_id)
        comment.delete()

        return url_

