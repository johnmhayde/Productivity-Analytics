from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login

def home(request):
    return render(request, 'portal/home.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            auth_login(request, new_user)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for { username }')
            return redirect('portal-home')
    else:
        form = UserCreationForm()
    return render(request, 'portal/register.html', {'form' : form})

def login(request):
    return render(request, 'portal/login.html')

def portal_home(request):
    return render(request, 'portal/portal_home.html')
