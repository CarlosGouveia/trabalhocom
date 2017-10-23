from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from .forms import RegisterForm

def login_view(request):

    if request.method=='POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Email ou senha incorretos!')
            return redirect('/')
    else:
        return redirect('/')

    return render(request, 'home.html')

def dashboard(request):
    template_name = 'accounts/dashboard.html'
    return render(request, template_name)

def register(request):
    template_name = 'accounts/register.html'
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(email=user.email, password=form.cleaned_data['password'])
            login(request, user)
            return redirect('core:home')
    else:
        form = RegisterForm()
    context = {
        'form': form
    }
    return render(request, template_name, context)