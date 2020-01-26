from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import GronnerRegisterForm

def index(request):
    if request.method == 'POST':
        form = GronnerRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('homepage')
    else:
        form = GronnerRegisterForm()
    return render(request, 'index/index.html', {'form':form})