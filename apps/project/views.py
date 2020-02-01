from django.shortcuts import render
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Project, Comment
from django.shortcuts import redirect
from apps.home.views import homepage
from django.contrib.auth.models import User
from .forms import CreateProject



class ProjectDetailView(DetailView):
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

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = CreateProject

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    fields = ['title', 'description', 'category']
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

    def test_func(self):
        project = self.get_object()
        if project.author == self.request.user:
            return True
        return False
