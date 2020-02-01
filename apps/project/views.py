from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, FormView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Project, Comment, Award, Medal
from django.shortcuts import redirect
from apps.home.views import homepage
from django.contrib.auth.models import User
from .forms import CreateProject
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import modelformset_factory


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
        context["top_projects"] = Project.objects.all().order_by('points')[:5]
        context["personal_projects"] = self.request.user.project_set.all().order_by('-date_posted')
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
        get_medals = Award.objects.filter(user=user, project=obj)

        if len(get_medals) == 0:
            Award.objects.create(user=user, medal=medal, project=obj)
        else: 
            if(Award.objects.get(user=user,project=obj).medal!=medal):
                get_medals.delete() 
                Award.objects.create(user=user, medal=medal, project=obj)
            else:
                get_medals.delete()         

        return url_

class ProjectCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Project
    form_class = CreateProject
    success_message = "Tu proyecto se ha subido correctamente"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    

class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    fields = ['title', 'description', 'category', 'image1', 'image2', 'image3']
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
        return False
