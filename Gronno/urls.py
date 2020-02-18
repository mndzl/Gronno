"""Gronno URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.users import views as user_views
from apps.home import views as home_views
from django.contrib.auth import views as auth_views
from apps.users.views import Profile, ProfileUpdateView, FollowView, FollowCategoryView
from apps.explore.views import CategoryExplore, Explore
from apps.about.views import privacy, about, conditions
from apps.project.views import (
    ProjectDetailView, 
    ProjectCreateView, 
    ProjectUpdateView, 
    ProjectDeleteView, 
    MedalToggle,
    ReportProject,
    CommentDelete,
)

urlpatterns = [
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='index/index.html'), name='logout'),

    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
    
    path('home/', home_views.homepage.as_view(), name='homepage'),
    path('notifications/', home_views.NotificationsView.as_view(), name='notifications'),

    path('users/<str:username>/', Profile.as_view(), name='profile'),
    path('users/<str:username>/follow/', FollowView.as_view(), name='follow'),
    path('users/config', ProfileUpdateView, name='config'),
    
    path('project/<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
    path('project/<int:pk>/<str:medal>', MedalToggle.as_view(), name='give_medal'),
    path('project/<int:pk>/update/', ProjectUpdateView.as_view(), name='project_update'),
    path('project/<int:pk>/delete/', ProjectDeleteView.as_view(), name='project_delete'),
    path('project/<int:pk>/report/<int:reason>', ReportProject.as_view(), name='report'),
    path('project/<int:pk_project>/delete_comment/<int:pk_comment>', CommentDelete.as_view(), name='comment_delete'),
    path('project/new/', ProjectCreateView.as_view(), name='project_create'),
    
    path('explore/<str:category>/', CategoryExplore.as_view(), name='category_explore'),
    path('explore/<str:category>/follow/', FollowCategoryView.as_view(), name='follow_category'),
    path('explore/', Explore, name='explore'),

    path('admin/', admin.site.urls),

    path('privacidad/', privacy, name='privacy'),
    path('acerca/', about, name='about'),

    path('', include('apps.index.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


#if settings.DEBUG:
#    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
