from django.shortcuts import render, redirect

def index(request):
    if request.user.username != "":
        return redirect('homepage')
    else:
        return render(request, 'index/index.html')