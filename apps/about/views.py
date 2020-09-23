from django.shortcuts import render
from apps.users.models import Notification

def privacy(request):
    context={
        'notifications': list(Notification.objects.filter(user=request.user).order_by('-date_created')[:5])
    }
    return render(request, 'about/privacy.html', context)

def conditions(request):
    context={
        'notifications': list(Notification.objects.filter(user=request.user).order_by('-date_created')[:5])
    }
    return render(request, 'about/conditions.html', context)

def about(request):
    context={
        'notifications': list(Notification.objects.filter(user=request.user).order_by('-date_created')[:5])
    }
    return render(request, 'about/about.html', context)
