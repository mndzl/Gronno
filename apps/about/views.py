from django.shortcuts import render

def privacy(request):
    return render(request, 'about/privacy.html')

def conditions(request):
    return render(request, 'about/conditions.html')

def about(request):
    return render(request, 'about/about.html')
